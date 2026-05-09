# CLAUDE.md — flet-wizards

Contexto completo do projeto para o Claude Code.
Leia este arquivo inteiro antes de qualquer ação.

---

## Visão geral

`flet-wizards` é um gallery app em Flet que demonstra templates de wizard multi-step reutilizáveis.
O objetivo atual é validar os templates visualmente e funcionalmente antes de publicar como biblioteca no PyPI.
O gallery funciona como um showcase estilo Microsoft Store: navegação lateral por categoria, cards com GIF de preview, e visualização ao vivo do template selecionado.

---

## Stack e ferramentas

- **Python**: 3.12+
- **Flet**: 0.85.0+ (auto-update ativo, sem `page.update()` manual em nenhuma circunstância)
- **Gerenciador de pacotes**: `uv` exclusivamente
- **Estrutura de projeto**: gerada via `flet create` (respeitar src/, assets/, storage/)
- **Logs**: `loguru` com rotatividade mínima (`rotation="1 MB"`, `retention=3`)
- **Documentação de código**: apenas docstrings técnicas inline, nada mais
- **Documentação de templates**: gerada pelo CocoIndex via CI/CD, não escrita manualmente

---

## Estrutura de diretórios

Estrutura real (inspecionada em 2026-05-09):

```
flet-wizards/
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── uv.lock
├── main.py                      ← leftover do `uv init`, não usar (entrypoint real é src/main.py)
├── docs/
│   └── reference/
│       └── wizard.py            ← referência visual e técnica, não modificar
├── pipeline/
│   ├── __init__.py
│   └── cocoindex_pipeline.py    ← gerador de docs via OpenAI
├── storage/
│   └── data/
│       └── app.log              ← criado em runtime pelo loguru
└── src/
    ├── assets/
    │   ├── icon.png
    │   └── splash_android.png
    ├── main.py                  ← entrypoint do gallery DEV (renderiza GalleryApp); fora do pacote PyPI
    ├── gallery/                 ← dev-only, NÃO entra no wheel publicado
    │   ├── __init__.py          ← exporta `state` (singleton observável de tema)
    │   ├── app.py               ← GalleryApp + ft.Router + GalleryShell + Header + WizardView + CategoryView + Redirect + NotFoundView
    │   ├── card.py              ← WizardCard
    │   └── sidebar.py           ← Sidebar (categorias + templates)
    └── flet_wizards/            ← pacote distribuído via PyPI
        ├── __init__.py          ← API pública: AuthLoginWizard, ProfileSetupWizard, …, WizardTheme
        ├── auth/
        │   ├── __init__.py
        │   ├── login.py
        │   ├── register.py
        │   └── recovery.py
        ├── core/
        │   ├── __init__.py      ← API interna re-exportada
        │   ├── base_state.py
        │   ├── base_wizard.py
        │   ├── components.py    ← divider, ghost_button, primary_button, form_field
        │   ├── mock_data.py     ← AUTH_LOGIN, AUTH_REGISTER, AUTH_RECOVERY, PROFILE_SETUP, PROFILE_EDIT, PROFILE_AVATAR
        │   ├── platform_guard.py
        │   ├── registry.py      ← WizardMeta + register/all_wizards/by_category/by_id/categories
        │   ├── snack.py         ← SnackHost + show_success/show_error/show_info
        │   └── theme.py
        └── profile/
            ├── __init__.py
            ├── avatar.py
            ├── edit.py
            └── setup.py
```

**Convenção crítica:** o pacote distribuído na PyPI é **`flet_wizards`** (com underscore — convenção Python). O nome do projeto/repo é **`flet-wizards`** (com hyphen — convenção PyPI/npm). `gallery/`, `pipeline/`, `src/main.py` e `src/assets/` são código de DESENVOLVIMENTO e ficam fora do wheel.

---

## Referência técnica obrigatória

Antes de criar qualquer wizard, leia `docs/reference/wizard.py`.
Esse arquivo é um wizard completo e publicado em produção. Ele define:

- O sistema de temas (`THEMES` dict com Slate, Emerald, Rose, Azure)
- O padrão de `AppState` com `@ft.observable` + `@dataclass`
- O padrão híbrido de estado: `ft.use_state` local sincronizado com estado global
- A estrutura do `Sidebar` com indicadores de step e conectores animados
- O `AnimatedSwitcher` com `key=str(state.step)` — obrigatório para transições corretas
- O `NavBar` com `async on_next` e loading state
- Os utilitários: `divider`, `ghost_button`, `primary_button`, `form_field`

Todos os wizards devem seguir esses padrões sem exceção.

---

## Padrões de código obrigatórios

### Estado reativo
```python
@ft.observable
@dataclass
class MeuWizardState(BaseWizardState):
    """Store reativo do wizard X."""
    campo: str = ""
```

### Componentes UI
```python
@ft.component
def MeuComponente(state: MeuWizardState) -> ft.Control:
    """Descrição técnica do que o componente renderiza."""
    ...
```

### Coroutines a partir de contexto síncrono
```python
page.run_task(minha_coroutine)
```

### Feedback ao usuário — ft.use_dialog()
Todo feedback visual (snackbar, confirmação, guard de plataforma) usa `ft.use_dialog()`.
Nunca usar `page.show_dialog()` diretamente nos wizards — centralizar em `core/snack.py`.

```python
# core/snack.py expõe:
show_success(page, mensagem)
show_error(page, mensagem)
show_info(page, mensagem)
```

Internamente cada helper usa `ft.use_dialog()` dentro de um `@ft.component`.

### Nunca usar
- `page.update()` em qualquer circunstância
- `page.show_snack()` — não existe no Flet 0.85.0
- Comentários inline (apenas docstrings)
- `setup.py` ou `requirements.txt`

---

## Recursos Flet 0.85.0 em uso neste projeto

### ft.Router
O gallery usa `ft.Router` com outlet para navegação declarativa entre categorias e templates.
Rotas definidas em `gallery/app.py`:

```
/                        → redireciona para /auth/login
/auth/<template_id>      → renderiza o wizard de auth correspondente
/profile/<template_id>   → renderiza o wizard de profile correspondente
```

O outlet substitui o conteúdo da área principal sem recriar a moldura do gallery.
`manage_views=False` — não usa view-stack, navegação é lateral não hierárquica.

### ft.use_dialog()
Hook declarativo para todo dialog do projeto. Usado em:
- `core/snack.py` — helpers de feedback (success, error, info)
- `core/platform_guard.py` — tela de plataforma incompatível com bypass

API real do `ft.use_dialog()` — assinatura inspecionada no runtime:
```python
ft.use_dialog(dialog: DialogControl | None = None)
```
Passa o `DialogControl` para exibir, `None` para fechar. É um hook — só funciona dentro de `@ft.component`.
Como os helpers precisam ser chamados de qualquer contexto (handlers async, callbacks), o padrão adotado é:
- `_SnackController` observável global com `show(msg, kind)` e `clear()`
- `SnackHost` (`@ft.component`) lê o controller e chama `ft.use_dialog(snack)` reativamente
- `SnackHost` é montado uma única vez no topo do app em `main.py`

---

## Sistema de temas

`WizardTheme` é uma dataclass em `core/theme.py` com os campos:
`primary`, `secondary`, `accent`, `bg`, `surface`, `card`, `panel`, `border`, `text`, `sub`

Built-ins disponíveis: `WizardTheme.SLATE`, `WizardTheme.EMERALD`, `WizardTheme.ROSE`, `WizardTheme.AZURE`

Paletas extraídas do `docs/reference/wizard.py` — usar exatamente os mesmos valores hex.

O tema padrão é `SLATE`. Todos os wizards aceitam um parâmetro `theme: WizardTheme` e reagem a mudanças via estado observável.

---

## Validação de plataforma

`core/platform_guard.py` recebe `supported_platforms: list[ft.PagePlatform]`.
Usa `page.platform` (não breakpoint de largura) para detecção.
Se a plataforma atual não estiver na lista, renderiza uma tela centralizada com:
- Ícone 📱
- Título "Template não compatível"
- Descrição das plataformas suportadas
- Botão ghost "Continuar mesmo assim" que bypassa o guard

Todos os wizards da versão inicial suportam todas as plataformas.
O guard existe para templates futuros mobile-only.

---

## WizardMeta — contrato obrigatório de cada template

Cada arquivo de wizard deve declarar uma instância de `WizardMeta` no topo.
Essa instância é a fonte de verdade para o gallery e para o pipeline CocoIndex.

```python
from flet_wizards.core.registry import WizardMeta

META = WizardMeta(
    id="auth.login",
    name="Login Clássico",
    category="auth",
    description="Wizard de login com e-mail e senha em dois steps.",
    steps=["Acesso", "Confirmação"],
    platforms=[ft.PagePlatform.WINDOWS, ft.PagePlatform.MACOS,
               ft.PagePlatform.LINUX, ft.PagePlatform.ANDROID,
               ft.PagePlatform.IOS],
    on_complete_schema={"email": "str"},
)
```

⚠️ `ft.PagePlatform` não tem `WEB` no Flet 0.85+. Use `page.web` (boolean) para detectar browser.

---

## Mock data

`core/mock_data.py` centraliza os dados de preenchimento automático para o modo demonstrativo do gallery.

Cada wizard recebe um parâmetro `mock: bool = False`. Quando `True`, o state é inicializado com os valores do dict correspondente. O gallery sempre passa `mock=True`. Quem importar a biblioteca futuramente usa `mock=False` por padrão.

```python
# core/mock_data.py

AUTH_LOGIN = {
    "email": "dev@exemplo.com",
    "password": "Senha@123",
}

AUTH_REGISTER = {
    "email": "dev@exemplo.com",
    "password": "Senha@123",
    "confirm_password": "Senha@123",
    "name": "Ada Lovelace",
    "role": "Dev",
}

AUTH_RECOVERY = {
    "email": "dev@exemplo.com",
    "code": "429731",
    "new_password": "NovaSenha@123",
    "confirm_password": "NovaSenha@123",
}

PROFILE_SETUP = {
    "name": "Ada Lovelace",
    "username": "ada.lovelace",
    "bio": "Engenheira de software apaixonada por sistemas distribuídos.",
    "interests": ["Python", "DevOps"],
    "theme_key": "Slate",
    "language": "pt-BR",
}

PROFILE_EDIT = {
    "name": "Ada Lovelace",
    "email": "dev@exemplo.com",
    "phone": "+55 11 91234-5678",
    "current_password": "",
    "new_password": "",
    "confirm": "",
}

PROFILE_AVATAR = {
    "source": "Iniciais",
    "initials": "AL",
    "bg_color": "#7C6EF6",
}
```

O wizard abre no **último step** por padrão no gallery (preview rápido). O dev pode navegar para o início clicando em "Voltar".

---

## Templates — especificações

### Auth

**auth/login.py — AuthLoginWizard**
Steps: "Acesso" (email + senha), "Confirmação" (card resumo + botão confirmar)
State: email, password
on_complete: `{"email": str}`

**auth/register.py — AuthRegisterWizard**
Steps: "Conta" (email + senha + confirmação), "Perfil" (nome + 6 chips de papel), "Confirmar" (card review com iniciais)
State: email, password, confirm_password, name, role
on_complete: `{"email": str, "name": str, "role": str}`

**auth/recovery.py — AuthRecoveryWizard**
Steps: "E-mail" (campo + instrução), "Código" (6 campos individuais lado a lado), "Nova senha" (nova + confirmação + indicador de força)
State: email, code, new_password, confirm_password
on_complete: `{"email": str}`

### Profile

**profile/setup.py — ProfileSetupWizard**
Steps: "Identidade" (nome + username), "Sobre" (bio textarea + 6 chips de interesse), "Preferências" (4 swatches de tema com troca ao vivo + dropdown de idioma)
State: name, username, bio, interests: list, theme_key, language
on_complete: `{"name": str, "username": str, "bio": str, "interests": list, "theme": str, "language": str}`

**profile/edit.py — ProfileEditWizard**
Recebe `initial_data: dict` para pré-popular campos.
Steps: "Dados" (nome + email + telefone), "Segurança" (senha atual + nova + confirmação), "Confirmar" (diff visual: só campos alterados em destaque)
State: name, email, phone, current_password, new_password, confirm
on_complete: `{"changed_fields": dict}`

**profile/avatar.py — ProfileAvatarWizard**
Steps: "Origem" (chips: Arquivo / URL / Iniciais), "Configurar" (conteúdo dinâmico por origem: FilePicker / campo URL com preview / campo iniciais + 6 swatches de cor), "Confirmar" (preview final)
State: source, file_path, url, initials, bg_color
on_complete: `{"source": str, "value": str}`

---

## Gallery app

`gallery/app.py — GalleryApp`

Layout estilo Microsoft Store:
- Sidebar esquerda (200px): seções "Auth" e "Profile" com rows clicáveis por template
- Header fixo: nome do template ativo + seletor de tema (4 círculos coloridos)
- Content view: área principal onde o conteúdo é substituído sem criar nova tela
  - Estado padrão: grid de cards dos templates da categoria selecionada
  - Ao clicar em "Visualizar": o wizard substitui o grid na mesma view via `AnimatedSwitcher`
  - O último step do wizard é aberto por padrão como preview rápido (com dados mock)
  - O dev pode navegar para o início clicando em "Voltar"

`gallery/card.py`
Card de template com: GIF de preview (ou screenshot estático), nome, descrição curta, badge de plataforma, botão "Visualizar".

`gallery/sidebar.py`
Navegação lateral por categoria. Item ativo destacado com `primary` do tema corrente.

---

## CocoIndex — pipeline de documentação

Localização: `pipeline/cocoindex_pipeline.py`

Roda via GitHub Actions a cada commit que altere arquivos em `src/flet_wizards/` ou `pipeline/`.
Lê todos os `META: WizardMeta` de cada template.
Gera via OpenAI API:
- `README.md` atualizado com tabela de todos os templates
- `docs/auth/login.md`, `docs/auth/register.md`, etc. — um arquivo por template

A chave da OpenAI é injetada como secret do GitHub (`OPENAI_API_KEY`).
O workflow faz commit automático com a mensagem `docs: regenerate from cocoindex pipeline`.

---

## Animações

Todas as animações usam:
```python
ft.Animation(300, ft.AnimationCurve.EASE_OUT_CUBIC)
```

`AnimatedSwitcher` usa `duration=260` com `FADE` transition, conforme referência.

---

## Storage — ft.StoragePaths

O app usa `ft.StoragePaths` para resolver caminhos reais em cada plataforma.
As pastas `storage/data/` e `storage/temp/` geradas pelo `flet create` servem apenas como fallback em desenvolvimento local.
`ft.StoragePaths` não funciona em modo web — tratar com `try/except FletUnsupportedPlatformException`.

Mapeamento de uso:

| Dado | Método | Motivo |
|---|---|---|
| Logs do loguru | `get_application_support_directory()` | Persistente, não exposto ao usuário |
| Tema ativo entre sessões | `get_application_documents_directory()` | Dado gerado pelo usuário, não recriável |
| Preview temporário de avatar | `get_temporary_directory()` | Pode ser limpo pelo sistema |
| Cache de GIFs dos cards | `get_application_cache_directory()` | Cache descartável |

Padrão de inicialização em `main.py`:

```python
async def main(page: ft.Page) -> None:
    storage = ft.StoragePaths()
    try:
        support_dir = await storage.get_application_support_directory()
        docs_dir = await storage.get_application_documents_directory()
        temp_dir = await storage.get_temporary_directory()
        cache_dir = await storage.get_application_cache_directory()
    except ft.FletUnsupportedPlatformException:
        support_dir = "storage/data"
        docs_dir = "storage/data"
        temp_dir = "storage/temp"
        cache_dir = "storage/temp"
```

Os caminhos resolvidos são passados para os módulos que precisam via parâmetro — nunca acessados como global.

---

## Logs

```python
from loguru import logger

# support_dir resolvido via ft.StoragePaths em main.py
logger.add(f"{support_dir}/app.log", rotation="1 MB", retention=3)
```

Usar `logger.debug`, `logger.info`, `logger.error` conforme a severidade.
Sem `print()` em nenhum arquivo.

---

## Publicação no PyPI

Build backend: **`hatchling`**. O pacote `flet_wizards` (com underscore) é o único módulo publicado — tudo de desenvolvimento (`gallery/`, `pipeline/`, `src/main.py`, `src/assets/`, `.github/`, `docs/`, `storage/`) fica fora do wheel via `[tool.hatch.build.targets.{wheel,sdist}]`.

### Fluxo de release

1. Bump `version` em `pyproject.toml` E em `src/flet_wizards/__init__.py` (`__version__`).
2. Commit + push: `chore: bump version to vX.Y.Z`.
3. Tag e push da tag:
   ```powershell
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. O workflow `.github/workflows/publish.yml` dispara automaticamente, builda via `uv build` e empurra pro PyPI via OIDC.

### Trusted Publisher (setup único)

**Sem `PYPI_API_TOKEN`** — usa OIDC via `pypa/gh-action-pypi-publish`. Requer cadastro do publisher no PyPI:

1. https://pypi.org/manage/account/publishing/ → "Add a new pending publisher" (na primeira release o projeto ainda não existe na PyPI; essa rota é a que funciona).
2. Preencher:
   - **PyPI Project Name**: `flet-wizards`
   - **Owner**: `Alisonsantos77`
   - **Repository name**: `flet-wizards`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
3. Criar o environment `pypi` em https://github.com/Alisonsantos77/flet-wizards/settings/environments (opcional mas recomendado — permite exigir review antes do publish).

### Validação local antes do tag

```powershell
uv build
ls dist/
```

Inspecionar o `.whl` com:
```powershell
uv run python -c "import zipfile; print('\n'.join(sorted(zipfile.ZipFile(next(iter(__import__('pathlib').Path('dist').glob('*.whl')))).namelist())))"
```

Esperado: APENAS `flet_wizards/...` + `flet_wizards-X.Y.Z.dist-info/...`. Se aparecer `gallery/`, `pipeline/`, `main.py`, etc., a config de exclude está errada.

---

## pyproject.toml — config real (resumido)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "flet-wizards"
version = "0.1.0"
description = "Multi-step wizard templates for Flet apps — auth, profile, and gallery showcase"
requires-python = ">=3.12"
license = { text = "MIT" }
dependencies = [
    "flet>=0.85.0",
    "loguru>=0.7.3",
]

[project.optional-dependencies]
pipeline = ["openai>=1.0.0"]   # só pra rodar pipeline/cocoindex_pipeline.py

[project.urls]
Homepage = "https://github.com/Alisonsantos77/flet-wizards"

[dependency-groups]
dev = [
    "flet-cli>=0.85.0",
    "flet-desktop>=0.85.0",
    "flet-web>=0.85.0",
]

[tool.hatch.build.targets.wheel]
packages = ["src/flet_wizards"]

[tool.hatch.build.targets.sdist]
include = ["src/flet_wizards", "README.md", "pyproject.toml"]
exclude = ["src/gallery", "src/main.py", "src/assets", "pipeline", ".github", "docs", "storage", "tests", "main.py"]

[tool.flet]
org = "com.alisonsantos"
product = "flet-wizards"

[tool.flet.app]
path = "src"
```

---

## Status do projeto

- [x] Scaffold via `uv init` + `flet create`
- [x] `core/` completo (theme, base_state, base_wizard, components, platform_guard, registry, snack, mock_data)
- [x] `auth/` completo (login, register, recovery)
- [x] `profile/` completo (setup, edit, avatar)
- [x] Refactor: `platform_guard.py` → `ft.use_dialog()`
- [x] Refactor: `base_wizard.py` → `core/snack.py` + `ft.use_dialog()`
- [x] Refactor: `main.py` → `ft.Router` (gallery substituiu o preview temporário)
- [x] `gallery/` completo (app, sidebar, card)
- [x] `pipeline/cocoindex_pipeline.py` — esqueleto inicial (script standalone, idempotência via hash em marker no topo do MD; payload inclui `class_name` e `module_path`)
- [x] GitHub Actions workflow (`.github/workflows/docs.yml`) — trigger em `src/flet_wizards/**` + `pipeline/**` + manual; auto-commit `docs: regenerate from cocoindex pipeline`
- [x] Refactor: `wizards/` → `flet_wizards/` (preparação PyPI, nome do pacote sem hyphen)
- [x] `pyproject.toml` com `hatchling` + exclude de gallery/pipeline; `src/flet_wizards/__init__.py` exporta API pública
- [x] `.github/workflows/publish.yml` — Trusted Publisher (OIDC), trigger em tags `v*`, sem `PYPI_API_TOKEN`
- [ ] Setup do Trusted Publisher na PyPI (manual: dashboard PyPI + create environment `pypi` no GitHub)
- [ ] Primeiro release v0.1.0 (após Trusted Publisher cadastrado): `git tag v0.1.0 && git push origin v0.1.0`
- [ ] Pipeline: integrar framework `cocoindex` propriamente (incremental + state tracking persistido) — hoje é script standalone
- [ ] GIFs de preview para cada template (substituir o placeholder em `gallery/card.py`)
- [ ] Limpar `main.py` da raiz (leftover do `uv init`)