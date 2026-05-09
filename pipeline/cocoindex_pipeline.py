"""Pipeline de geração de documentação dos wizards via OpenAI.

Lê todos os `WizardMeta` do registry (populado pelos imports dos
módulos de wizards) e produz, na raiz do repo:

  - `docs/<categoria>/<template>.md` — um arquivo por template
  - `README.md` — visão geral com tabela de todos os templates

Disparado via GitHub Actions em commits que alteram `src/wizards/`.
A chave da OpenAI vem de `OPENAI_API_KEY` (secret do repositório).

## Idempotência

Cada doc gerado começa com um marker `<!-- generated-from-hash: XXX -->`
contendo o hash SHA-256 (16 chars) da meta serializada. Antes de chamar
OpenAI, o pipeline compara o hash corrente com o do arquivo existente:
se igual, pula (sem custo). Se diferente ou se o arquivo não existe,
regenera. README é sempre re-renderizado (não usa OpenAI).

## Status

Implementação inicial **standalone** — não usa o framework `cocoindex`
propriamente. O nome do arquivo segue o spec do CLAUDE.md; migração
para `flow_def` do cocoindex fica como TODO quando precisar de tracking
incremental persistido (ex: detectar deleção de wizard entre runs).

## Execução local

```powershell
$env:OPENAI_API_KEY = "sk-..."
uv run --extra pipeline python pipeline/cocoindex_pipeline.py
```
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DOCS_DIR = PROJECT_ROOT / "docs"
README_PATH = PROJECT_ROOT / "README.md"

sys.path.insert(0, str(SRC_DIR))

import wizards.auth.login  # noqa: E402, F401
import wizards.auth.recovery  # noqa: E402, F401
import wizards.auth.register  # noqa: E402, F401
import wizards.profile.avatar  # noqa: E402, F401
import wizards.profile.edit  # noqa: E402, F401
import wizards.profile.setup  # noqa: E402, F401

from wizards.core import (  # noqa: E402
    WizardMeta,
    all_wizards,
    by_category,
    categories,
)

MODEL = "gpt-4o-mini"
HASH_MARKER = "<!-- generated-from-hash: "
HASH_END = " -->"

SYSTEM_PROMPT = """Você é um gerador de documentação técnica para uma biblioteca Python de wizards multi-step em Flet.

Receberá um JSON com a metadata de um template (id, nome, categoria, descrição, steps, plataformas suportadas, schema de retorno do on_complete).

Devolva APENAS Markdown em português, técnico e direto, com EXATAMENTE esta estrutura:

# {name}

> {description}

## Steps

Tabela com colunas `#` e `Nome` listando cada step na ordem.

## Plataformas suportadas

Lista bullet das plataformas (ex: Windows, macOS, Linux, Android, iOS).

## Retorno do `on_complete`

Tabela com colunas `Campo` e `Tipo` derivada do schema. Quando o schema estiver vazio, escreva "Nenhum dado é retornado.".

## Uso

Bloco de código Python concreto mostrando como instanciar o wizard com `theme=`, `on_complete=` e tratando o callback. Use `from wizards.<categoria>.<arquivo> import <ClasseWizard>`.

## Mock no gallery

Uma frase explicando que o wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews.

NÃO inclua introdução, conclusão, header HTML ou qualquer texto fora dessa estrutura. NÃO use placeholders genéricos como `[seu app]`; use exemplos concretos baseados nos campos do schema.
"""


def _meta_to_dict(meta: WizardMeta) -> dict:
    """Serialização canônica usada tanto na hash quanto no payload OpenAI."""
    return {
        "id": meta.id,
        "name": meta.name,
        "category": meta.category,
        "description": meta.description,
        "steps": list(meta.steps),
        "platforms": [p.name for p in meta.platforms],
        "on_complete_schema": dict(meta.on_complete_schema),
    }


def _meta_hash(meta: WizardMeta) -> str:
    """SHA-256 truncado em 16 chars do JSON canônico da meta."""
    blob = json.dumps(_meta_to_dict(meta), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def _existing_hash(path: Path) -> str | None:
    """Lê o hash do marker no topo do arquivo, ou None se não existir."""
    if not path.exists():
        return None
    head = path.read_text(encoding="utf-8")[:200]
    if HASH_MARKER not in head:
        return None
    start = head.index(HASH_MARKER) + len(HASH_MARKER)
    end = head.index(HASH_END, start)
    return head[start:end].strip()


def _doc_path(meta: WizardMeta) -> Path:
    """`docs/<categoria>/<template>.md` derivado do meta.id ('cat.tid')."""
    parts = meta.id.split(".", 1)
    template = parts[1] if len(parts) > 1 else meta.id
    return DOCS_DIR / meta.category / f"{template}.md"


def _generate_doc(meta: WizardMeta, client) -> str:
    """Chama OpenAI e devolve o Markdown completo (com marker de hash no topo)."""
    user_payload = json.dumps(_meta_to_dict(meta), ensure_ascii=False, indent=2)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_payload},
        ],
        temperature=0.2,
    )
    body = response.choices[0].message.content.strip()
    marker = f"{HASH_MARKER}{_meta_hash(meta)}{HASH_END}\n\n"
    return marker + body + "\n"


def _render_readme(metas: list[WizardMeta]) -> str:
    """Tabela de todos os templates + bloco de uso. Sem chamada OpenAI."""
    lines = [
        "# flet-wizards",
        "",
        "Gallery de templates de wizard multi-step para Flet, prontos para reuso.",
        "",
        "## Templates disponíveis",
        "",
        "| Categoria | Nome | Steps | Descrição |",
        "|-----------|------|-------|-----------|",
    ]
    for cat in categories():
        for meta in by_category(cat):
            doc_link = _doc_path(meta).relative_to(PROJECT_ROOT).as_posix()
            lines.append(
                f"| {cat} | [{meta.name}]({doc_link}) | {len(meta.steps)} | {meta.description} |"
            )
    lines += [
        "",
        "## Uso rápido",
        "",
        "```python",
        "import flet as ft",
        "from wizards.auth.login import AuthLoginWizard",
        "",
        "async def main(page: ft.Page):",
        "    page.render(lambda: AuthLoginWizard(on_complete=lambda d: print(d)))",
        "",
        "ft.run(main)",
        "```",
        "",
        "## Gallery",
        "",
        "```powershell",
        "uv run flet run",
        "```",
        "",
        "Abre o showcase com sidebar por categoria, seletor de tema (4 paletas) e preview ao vivo de cada template.",
        "",
        "---",
        "",
        "_Documentação regenerada automaticamente por `pipeline/cocoindex_pipeline.py`._",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY não definida — abortando")
        sys.exit(1)

    try:
        from openai import OpenAI
    except ImportError:
        logger.error(
            "openai não instalado — rode `uv sync --extra pipeline` ou adicione manualmente"
        )
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    metas = all_wizards()
    logger.info("Encontrados {} wizards no registry", len(metas))

    regenerated = 0
    skipped = 0
    for meta in metas:
        path = _doc_path(meta)
        new_hash = _meta_hash(meta)
        if _existing_hash(path) == new_hash:
            logger.info("[skip] {} (hash inalterado)", meta.id)
            skipped += 1
            continue

        logger.info("[gen]  {} → {}", meta.id, path.relative_to(PROJECT_ROOT))
        content = _generate_doc(meta, client)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        regenerated += 1

    readme = _render_readme(metas)
    README_PATH.write_text(readme, encoding="utf-8")
    logger.info("README.md atualizado com {} wizards", len(metas))
    logger.info("Concluído: {} regenerado(s), {} ignorado(s)", regenerated, skipped)


if __name__ == "__main__":
    main()
