<!-- generated-from-hash: df881d416a58175e -->

# Setup de Perfil

> Wizard de onboarding com identidade, interesses e preferências.

## Steps

| #  | Nome         |
|----|--------------|
| 1  | Identidade   |
| 2  | Sobre        |
| 3  | Preferências  |

## Campos por step

### 1. Identidade
- **name** (`str`) — Nome completo do usuário.
- **username** (`str`) — Nome de usuário desejado.

### 2. Sobre
- **bio** (`str`) — Breve descrição sobre o usuário.

### 3. Preferências
- **interests** (`list`) — Lista de interesses do usuário.
- **theme** (`str`) — Tema preferido para a interface.
- **language** (`str`) — Idioma preferido do usuário.

## Plataformas suportadas

- Windows
- macOS
- Linux
- Android
- iOS

## Retorno do `on_complete`

| Campo     | Tipo  |
|-----------|-------|
| name      | str   |
| username  | str   |
| bio       | str   |
| interests  | list  |
| theme     | str   |
| language  | str   |

## Uso

```python
import flet as ft
from wizards.profile.setup import ProfileSetupWizard
from wizards.core import WizardTheme


async def main(page: ft.Page) -> None:
    async def on_complete(data: dict) -> None:
        print(data["name"])
        print(data["username"])
        print(data["bio"])
        print(data["interests"])
        print(data["theme"])
        print(data["language"])

    page.render(lambda: ProfileSetupWizard(
        theme=WizardTheme.SLATE,
        on_complete=on_complete,
    ))


ft.run(main)
```

Mock no gallery: O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews dentro do gallery showcase.
