# flet-wizards

🌐 [Português](README.pt-BR.md) | **English**

[![PyPI version](https://img.shields.io/pypi/v/flet-wizards.svg)](https://pypi.org/project/flet-wizards/)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Flet](https://img.shields.io/badge/flet-0.85+-purple.svg)](https://flet.dev)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

Ready-made multi-step wizard templates for Flet — authentication, profile, onboarding and survey.
Each template is a self-contained `@ft.component` with reactive state, a dark/light theme system and a typed `on_complete` callback.

---

## Installation

```bash
pip install flet-wizards
```

Requires **Python 3.12+** and **Flet 0.85+**.

---

## Quick start

```python
import flet as ft
from flet_wizards import AuthLoginWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_login(data: dict) -> None:
        email = data["email"]
        # authenticate...

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

Every wizard is imported from the package root:

```python
from flet_wizards import (
    AuthLoginWizard, AuthRegisterWizard, AuthRecoveryWizard, AuthTwoFactorWizard,
    ProfileSetupWizard, ProfileEditWizard, ProfileAvatarWizard,
    OnboardingWalkthroughWizard, SurveyFeedbackWizard,
    WizardTheme,
)
```

---

## Available templates

| Category | Class | Steps | Description | Docs |
|---|---|---|---|---|
| `auth` | `AuthLoginWizard` | 2 | Email and password login plus confirmation screen. | [docs/auth/login.md](docs/auth/login.md) |
| `auth` | `AuthRegisterWizard` | 3 | Sign-up with account, profile and review. | [docs/auth/register.md](docs/auth/register.md) |
| `auth` | `AuthRecoveryWizard` | 3 | Password recovery with a 6-digit code and animated strength meter. | [docs/auth/recovery.md](docs/auth/recovery.md) |
| `auth` | `AuthTwoFactorWizard` | 1 | Mobile-first 2FA verification with six individual digits. | [docs/auth/two_factor.md](docs/auth/two_factor.md) |
| `profile` | `ProfileSetupWizard` | 3 | Onboarding with identity, bio, interests and preferences. | [docs/profile/setup.md](docs/profile/setup.md) |
| `profile` | `ProfileEditWizard` | 3 | Editing flow with a visual diff highlighting only the changed fields. | [docs/profile/edit.md](docs/profile/edit.md) |
| `profile` | `ProfileAvatarWizard` | 3 | Avatar via URL or initials with live preview. | [docs/profile/avatar.md](docs/profile/avatar.md) |
| `onboarding` | `OnboardingWalkthroughWizard` | 4 | Mobile fullscreen walkthrough across 4 slides. | [docs/onboarding/walkthrough.md](docs/onboarding/walkthrough.md) |
| `survey` | `SurveyFeedbackWizard` | 3 | Conversational survey with NPS, comment and category. | [docs/survey/feedback.md](docs/survey/feedback.md) |

`AuthTwoFactorWizard`, `OnboardingWalkthroughWizard` and `SurveyFeedbackWizard` are mobile-first (Android / iOS). When opened on desktop, `PlatformGuard` shows a notice with a "Continue anyway" button.

---

## Themes

The library exposes 7 theme pairs, each with two variants (dark and light), for a total of 14 internal palettes. You pick a theme by the pair name:

| Pair | Dark primary | Light primary |
|---|---|---|
| Slate | `#7C6EF6` | `#6366F1` |
| Emerald | `#6EE7B7` | `#059669` |
| Rose | `#FB7185` | `#E11D48` |
| Azure | `#818CF8` | `#4F46E5` |
| Amber | `#F59E0B` | `#D97706` |
| Crimson | `#DE1F26` | `#B91C1C` |
| Frost | `#60A5FA` | `#0052FF` |

### Direct use

```python
from flet_wizards import WizardTheme

AuthLoginWizard(theme=WizardTheme.SLATE)        # dark variant
AuthLoginWizard(theme=WizardTheme.SLATE_LIGHT)  # light variant
```

### Automatic detection (system dark/light)

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

`resolve_theme(theme, mode)` returns the correct variant:
- `ft.ThemeMode.DARK` → dark variant of the pair.
- `ft.ThemeMode.LIGHT` → light variant of the pair.
- `ft.ThemeMode.SYSTEM` → reads `page.platform_brightness` and falls back to dark when outside a reactive context.

Full details in [docs/themes.md](docs/themes.md).

---

## Local development preview

To inspect the wizards visually during development:

```powershell
git clone https://github.com/Alisonsantos77/flet-wizards
cd flet-wizards
uv sync
uv run flet run
```

This opens a window with all 9 templates side by side, including theme and dark/light mode selectors. The preview code lives in `src/gallery/` and is **not** part of the package published on PyPI — it is a local inspection tool only.

---

## Live demo

See every template running live in the companion demo project:

[flet-wizards-gallery](https://github.com/Alisonsantos77/flet-wizards-gallery)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidance on adding new templates and the project conventions.

---

## License

[MIT](./LICENSE) © Alison Santos
