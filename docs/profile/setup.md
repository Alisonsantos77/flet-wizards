<!-- generated-from-hash: 29fc2bc9505b8d97 -->

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
- **name** (`str`) — nome do usuário.
- **username** (`str`) — nome de usuário escolhido.

### 2. Sobre
- **bio** (`str`) — biografia ou descrição pessoal.

### 3. Preferências
- **interests** (`list`) — lista de interesses do usuário.
- **theme** (`str`) — tema preferido da interface.
- **language** (`str`) — idioma preferido.

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
from flet_wizards.profile.setup import ProfileSetupWizard
from flet_wizards.core import WizardTheme


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
