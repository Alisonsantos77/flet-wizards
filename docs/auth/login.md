<!-- generated-from-hash: 36cee0e2bfe8eeba -->

# Login Clássico

> Wizard de login com e-mail e senha em dois steps.

## Steps

| #  | Nome          |
|----|---------------|
| 1  | Acesso        |
| 2  | Confirmação   |

## Campos por step

### 1. Acesso
- **email** (str) — e-mail do usuário.

### 2. Confirmação
_Não captura dados novos — apenas revisa o que foi preenchido._

## Plataformas suportadas

- Windows
- macOS
- Linux
- Android
- iOS

## Retorno do `on_complete`

| Campo  | Tipo |
|--------|------|
| email  | str  |

## Uso

```python
import flet as ft
from wizards.auth.login import AuthLoginWizard
from wizards.core import WizardTheme


async def main(page: ft.Page) -> None:
    async def on_complete(data: dict) -> None:
        print(data["email"])

    page.render(lambda: AuthLoginWizard(
        theme=WizardTheme.SLATE,
        on_complete=on_complete,
    ))


ft.run(main)
```

Mock no gallery: o wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews dentro do gallery showcase.
