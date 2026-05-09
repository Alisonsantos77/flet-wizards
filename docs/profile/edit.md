<!-- generated-from-hash: 8578e90b74687430 -->

# Editar Perfil

> Wizard de edição de perfil com diff visual no resumo.

## Steps

| #  | Nome        |
|----|-------------|
| 1  | Dados       |
| 2  | Segurança   |
| 3  | Confirmar   |

## Campos por step

### 1. Dados
- **changed_fields** (dict) — campos que foram alterados no perfil.

### 2. Segurança
- _Não captura dados novos — apenas revisa o que foi preenchido._

### 3. Confirmar
- _Não captura dados novos — apenas revisa o que foi preenchido._

## Plataformas suportadas

- Windows
- macOS
- Linux
- Android
- iOS

## Retorno do `on_complete`

| Campo         | Tipo  |
|---------------|-------|
| changed_fields| dict  |

## Uso

```python
import flet as ft
from wizards.profile.edit import ProfileEditWizard
from wizards.core import WizardTheme


async def main(page: ft.Page) -> None:
    async def on_complete(data: dict) -> None:
        print(data["changed_fields"])

    page.render(lambda: ProfileEditWizard(
        theme=WizardTheme.SLATE,
        on_complete=on_complete,
    ))


ft.run(main)
```

Mock no gallery: O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews dentro do gallery showcase.
