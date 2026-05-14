# flet-wizards

[![PyPI version](https://img.shields.io/pypi/v/flet-wizards.svg)](https://pypi.org/project/flet-wizards/)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Flet](https://img.shields.io/badge/flet-0.85+-purple.svg)](https://flet.dev)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

Templates de wizard multi-step prontos para Flet — autenticação, perfil, onboarding e survey.
Cada template é uma `@ft.component` autocontida com estado reativo, sistema de temas dark/light e callback `on_complete` tipado.

---

## Instalação

```bash
pip install flet-wizards
```

Requer **Python 3.12+** e **Flet 0.85+**.

---

## Uso rápido

```python
import flet as ft
from flet_wizards import AuthLoginWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_login(data: dict) -> None:
        email = data["email"]
        # autenticar...

    return AuthLoginWizard(
        theme=WizardTheme.SLATE,
        on_complete=handle_login,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.bgcolor = "#0B0B0F"
    page.render(App)


ft.run(main)
```

Todos os wizards são importados a partir da raiz do pacote:

```python
from flet_wizards import (
    AuthLoginWizard, AuthRegisterWizard, AuthRecoveryWizard, AuthTwoFactorWizard,
    ProfileSetupWizard, ProfileEditWizard, ProfileAvatarWizard,
    OnboardingWalkthroughWizard, SurveyFeedbackWizard,
    WizardTheme,
)
```

---

## Templates disponíveis

| Categoria | Classe | Steps | Descrição | Docs |
|---|---|---|---|---|
| `auth` | `AuthLoginWizard` | 2 | Login com e-mail e senha + tela de confirmação. | [docs/auth/login.md](docs/auth/login.md) |
| `auth` | `AuthRegisterWizard` | 3 | Cadastro com conta, perfil e revisão. | [docs/auth/register.md](docs/auth/register.md) |
| `auth` | `AuthRecoveryWizard` | 3 | Recuperação de senha com código de 6 dígitos e força animada. | [docs/auth/recovery.md](docs/auth/recovery.md) |
| `auth` | `AuthTwoFactorWizard` | 1 | Verificação 2FA mobile-first com 6 dígitos individuais. | [docs/auth/two_factor.md](docs/auth/two_factor.md) |
| `profile` | `ProfileSetupWizard` | 3 | Onboarding com identidade, bio, interesses e preferências. | [docs/profile/setup.md](docs/profile/setup.md) |
| `profile` | `ProfileEditWizard` | 3 | Edição com diff visual destacando apenas campos alterados. | [docs/profile/edit.md](docs/profile/edit.md) |
| `profile` | `ProfileAvatarWizard` | 3 | Avatar via URL ou iniciais com preview ao vivo. | [docs/profile/avatar.md](docs/profile/avatar.md) |
| `onboarding` | `OnboardingWalkthroughWizard` | 4 | Walkthrough mobile fullscreen em 4 slides. | [docs/onboarding/walkthrough.md](docs/onboarding/walkthrough.md) |
| `survey` | `SurveyFeedbackWizard` | 3 | Survey conversacional com NPS, comentário e categoria. | [docs/survey/feedback.md](docs/survey/feedback.md) |

Os wizards `AuthTwoFactorWizard`, `OnboardingWalkthroughWizard` e `SurveyFeedbackWizard` são mobile-first (Android / iOS). Quando abertos em desktop, o `PlatformGuard` exibe aviso com botão "Continuar mesmo assim".

---

## Temas

A lib expõe 7 pares de temas, cada um em duas variantes (dark e light), totalizando 14 paletas internas. O dev escolhe pelo nome do par:

| Par | Dark primary | Light primary |
|---|---|---|
| Slate | `#7C6EF6` | `#6366F1` |
| Emerald | `#6EE7B7` | `#059669` |
| Rose | `#FB7185` | `#E11D48` |
| Azure | `#818CF8` | `#4F46E5` |
| Amber | `#F59E0B` | `#D97706` |
| Crimson | `#DE1F26` | `#B91C1C` |
| Frost | `#60A5FA` | `#0052FF` |

### Uso direto

```python
from flet_wizards import WizardTheme

AuthLoginWizard(theme=WizardTheme.SLATE)        # variante dark
AuthLoginWizard(theme=WizardTheme.SLATE_LIGHT)  # variante light
```

### Detecção automática (dark/light do sistema)

```python
import flet as ft
from flet_wizards import AuthLoginWizard, WizardTheme
from flet_wizards.core import resolve_theme


@ft.component
def App() -> ft.Control:
    page = ft.context.page
    theme = resolve_theme(WizardTheme.SLATE, page.theme_mode)
    return AuthLoginWizard(theme=theme)
```

`resolve_theme(theme, mode)` devolve a variante correta:
- `ft.ThemeMode.DARK` → variante dark do par.
- `ft.ThemeMode.LIGHT` → variante light do par.
- `ft.ThemeMode.SYSTEM` → consulta `page.platform_brightness` e cai em dark como fallback fora de contexto reativo.

Detalhes em [docs/themes.md](docs/themes.md).

---

## Preview local de desenvolvimento

Para inspecionar os wizards visualmente durante o desenvolvimento:

```powershell
git clone https://github.com/Alisonsantos77/flet-wizards
cd flet-wizards
uv sync
uv run flet run
```

Abre uma janela com todos os 9 templates lado a lado, com seletor de tema e modo dark/light. O código do preview vive em `src/gallery/` e **não** faz parte do pacote distribuído no PyPI — é apenas ferramenta de inspeção local.

---

## Demo interativa

Veja todos os templates ao vivo no projeto de demonstração:

[flet-wizards-gallery](https://github.com/Alisonsantos77/flet-wizards-gallery)

---

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para instruções de como adicionar templates e convenções do projeto.

---

## Licença

[MIT](./LICENSE) © Alison Santos
