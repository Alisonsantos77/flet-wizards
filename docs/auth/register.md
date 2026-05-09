<!-- generated-from-hash: 2e1304e38e43496b -->

# Cadastro

> Wizard de cadastro com conta, perfil e confirmação.

## Steps

| #  | Nome      |
|----|-----------|
| 1  | Conta     |
| 2  | Perfil    |
| 3  | Confirmar |

## Campos por step

### 1. Conta
- **email** (`str`) — endereço de e-mail do usuário.

### 2. Perfil
- **name** (`str`) — nome do usuário.
- **role** (`str`) — papel ou função do usuário.

### 3. Confirmar
_Não captura dados novos — apenas revisa o que foi preenchido._

## Plataformas suportadas

- Windows
- macOS
- Linux
- Android
- iOS

## Retorno do `on_complete`

| Campo | Tipo |
|-------|------|
| email | str  |
| name  | str  |
| role  | str  |

## Uso

```python
import flet as ft
from wizards.auth.register import AuthRegisterWizard
from wizards.core import WizardTheme


async def main(page: ft.Page) -> None:
    async def on_complete(data: dict) -> None:
        print(data["email"])
        print(data["name"])
        print(data["role"])

    page.render(lambda: AuthRegisterWizard(
        theme=WizardTheme.SLATE,
        on_complete=on_complete,
    ))


ft.run(main)
```

Mock no gallery: O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews dentro do gallery showcase.
