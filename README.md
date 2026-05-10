# flet-wizards

[![PyPI version](https://img.shields.io/pypi/v/flet-wizards.svg)](https://pypi.org/project/flet-wizards/)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Flet](https://img.shields.io/badge/flet-0.85+-purple.svg)](https://flet.dev)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

Coleção de templates de wizard multi-step prontos para reutilizar em apps Flet. Cada template é uma `@ft.component` autocontida com estado reativo (`@ft.observable`), sistema de temas (Slate / Emerald / Rose / Azure), validação de plataforma e callback `on_complete` tipado. O repositório inclui um **gallery showcase** estilo Microsoft Store para visualizar todos os templates ao vivo durante o desenvolvimento.

---

## Templates disponíveis

| Categoria | Template | Steps | Descrição | Docs |
|---|---|---|---|---|
| `auth` | `AuthLoginWizard` | 2 | Login clássico com e-mail e senha. | [docs/auth/login.md](docs/auth/login.md) |
| `auth` | `AuthRegisterWizard` | 3 | Cadastro com conta, perfil e revisão. | [docs/auth/register.md](docs/auth/register.md) |
| `auth` | `AuthRecoveryWizard` | 3 | Recuperação de senha com código de 6 dígitos e força animada. | [docs/auth/recovery.md](docs/auth/recovery.md) |
| `profile` | `ProfileSetupWizard` | 3 | Onboarding com identidade, bio, interesses e preferências (tema ao vivo). | [docs/profile/setup.md](docs/profile/setup.md) |
| `profile` | `ProfileEditWizard` | 3 | Edição com diff visual destacando apenas campos alterados. | [docs/profile/edit.md](docs/profile/edit.md) |
| `profile` | `ProfileAvatarWizard` | 3 | Configuração de avatar via arquivo, URL ou iniciais com preview. | [docs/profile/avatar.md](docs/profile/avatar.md) |

---

## Instalação

```bash
pip install flet-wizards
```

Ou com [uv](https://docs.astral.sh/uv/):

```bash
uv add flet-wizards
```

Requer **Python 3.12+** e **Flet 0.85+**.

---

## Uso rápido

```python
import flet as ft
from flet_wizards import AuthLoginWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def on_login(data: dict) -> None:
        print("Login:", data)
        # data == {"email": "..."}

    return AuthLoginWizard(
        theme=WizardTheme.SLATE,
        on_complete=on_login,
    )


async def main(page: ft.Page) -> None:
    page.title = "Meu app"
    page.padding = 0
    page.bgcolor = "#0B0B0F"
    page.render(App)


ft.run(main)
```

Os 4 temas built-in são acessados via `WizardTheme.SLATE`, `WizardTheme.EMERALD`, `WizardTheme.ROSE` e `WizardTheme.AZURE`. Quem precisar de uma paleta customizada constrói uma `WizardTheme(...)` própria — todos os campos são strings hex.

---

## Gallery

O repositório vem com um app de demonstração que renderiza todos os templates lado a lado, com seletor de tema e navegação por categoria:

```powershell
git clone https://github.com/Alisonsantos77/flet-wizards
cd flet-wizards
uv sync
uv run flet run
```

A janela abre em **1280×820** com sidebar por categoria (Auth / Profile), header com 4 swatches de tema e área principal mostrando o template selecionado em modo `mock=True` (já preenchido com dados de exemplo, abrindo direto no último step de dados como preview rápido).

---

## Contribuindo

### 1. Setup local

```powershell
git clone https://github.com/Alisonsantos77/flet-wizards
cd flet-wizards
uv sync
uv run flet run
```

### 2. Estrutura

- `src/flet_wizards/` — pacote distribuído via PyPI (o que vai no wheel).
- `src/gallery/` — showcase de desenvolvimento, **fora do wheel**.
- `src/main.py` — entrypoint do `flet run` para o gallery, **fora do wheel**.
- `docs/` — documentação técnica de cada template (escrita manualmente, lendo o código fonte).

### 3. Adicionar um novo template

1. **Criar o módulo** em `src/flet_wizards/<categoria>/<nome>.py`. Decidir a categoria (existentes: `auth`, `profile`; novas categorias podem ser criadas livremente — o gallery descobre automaticamente via registry).

2. **Declarar o `WizardMeta`** no topo do módulo, registrando-o no índice global:

   ```python
   from flet_wizards.core import WizardMeta, register

   META = register(
       WizardMeta(
           id="categoria.nome",          # ID único, ex.: "auth.magic_link"
           name="Nome do Template",      # exibido no card do gallery
           category="categoria",         # bucket no sidebar
           description="Descrição curta para o card.",
           steps=["Step 1", "Step 2"],   # labels do Sidebar interno
           platforms=[                   # plataformas suportadas
               ft.PagePlatform.WINDOWS,
               ft.PagePlatform.MACOS,
               ft.PagePlatform.LINUX,
               ft.PagePlatform.ANDROID,
               ft.PagePlatform.IOS,
           ],
           on_complete_schema={"campo": "str"},   # documenta o payload
       )
   )
   ```

3. **Definir o state reativo** estendendo `BaseWizardState`:

   ```python
   from dataclasses import dataclass
   from typing import ClassVar
   import flet as ft
   from flet_wizards.core import BaseWizardState

   @ft.observable
   @dataclass
   class MeuState(BaseWizardState):
       TOTAL_STEPS: ClassVar[int] = 2  # número de steps de DADOS (sucesso é o N+1)
       campo: str = ""

       def reset(self) -> None:
           super().reset()
           self.campo = ""
   ```

4. **Criar os step components** em escopo de módulo (nunca aninhados — o registro de hooks quebra). Cada um decorado com `@ft.component` e recebe `state` como parâmetro.

5. **Construir o wizard público** com `WizardFrame`, passando `state`, `step_labels`, `step_hints`, `steps` (lista de componentes incluindo o de sucesso) e `on_complete`. Aceitar `mock: bool = False` para ativar o preview do gallery.

6. **Adicionar mock data** em `src/flet_wizards/core/mock_data.py` se o template precisar:

   ```python
   MEU_TEMPLATE = {"campo": "valor de exemplo"}
   ```

7. **Re-exportar** no `src/flet_wizards/__init__.py`:

   ```python
   from flet_wizards.<categoria>.<nome> import MeuWizard
   __all__ = [..., "MeuWizard"]
   ```

8. **Registrar no gallery** importando o módulo em `src/gallery/app.py` (basta o import — `register()` é idempotente e o `WizardCard` é renderizado a partir do registry).

9. **Documentar** criando `docs/<categoria>/<nome>.md` com as seções: descrição, steps, campos por step, plataformas, retorno do `on_complete`, exemplo de uso e mock no gallery.

10. **Atualizar a tabela** de templates neste README e a entrada no `CHANGELOG.md`.

### 4. Convenções

- **Sem `page.update()`** em nenhuma circunstância — Flet 0.85+ tem auto-update.
- **Apenas docstrings** como documentação inline; sem comentários de linha.
- **Logs com `loguru`**, sem `print()`.
- **Feedback visual** sempre via helpers de `flet_wizards.core.snack` (`show_success`, `show_error`, `show_info`), nunca `page.show_dialog()` direto.

---

## Licença

[MIT](LICENSE) © Alison Santos.
