<!-- generated-from-hash: a536bf3b4f618de3 -->

# Recuperar Senha

> Wizard de recuperação de senha com código de verificação.

## Steps

| #  | Nome         |
|----|--------------|
| 1  | E-mail       |
| 2  | Código       |
| 3  | Nova senha   |

## Campos por step

### 1. E-mail
- **email** (`str`) — endereço de e-mail do usuário.

### 2. Código
- _Não captura dados novos — apenas revisa o que foi preenchido._

### 3. Nova senha
- _Não captura dados novos — apenas revisa o que foi preenchido._

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

## Uso

```python
import flet as ft
from flet_wizards.auth.recovery import AuthRecoveryWizard
from flet_wizards.core import WizardTheme


async def main(page: ft.Page) -> None:
    async def on_complete(data: dict) -> None:
        print(data["email"])

    page.render(lambda: AuthRecoveryWizard(
        theme=WizardTheme.SLATE,
        on_complete=on_complete,
    ))


ft.run(main)
```

Mock no gallery: O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews dentro do gallery showcase.
