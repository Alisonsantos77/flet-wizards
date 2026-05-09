<!-- generated-from-hash: 0ea0457cc561ede1 -->

# Avatar

> Wizard de configuração de avatar com 3 origens (arquivo, URL, iniciais).

## Steps

| # | Nome       |
|---|------------|
| 1 | Origem     |
| 2 | Configurar  |
| 3 | Confirmar  |

## Campos por step

### 1. Origem
- **source** (str) — origem do avatar (arquivo, URL ou iniciais).

### 2. Configurar
- **value** (str) — valor do avatar configurado.

### 3. Confirmar
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
| source | str  |
| value  | str  |

## Uso

```python
import flet as ft
from flet_wizards.profile.avatar import ProfileAvatarWizard
from flet_wizards.core import WizardTheme


async def main(page: ft.Page) -> None:
    async def on_complete(data: dict) -> None:
        print(data["source"])
        print(data["value"])

    page.render(lambda: ProfileAvatarWizard(
        theme=WizardTheme.SLATE,
        on_complete=on_complete,
    ))


ft.run(main)
```

Mock no gallery: O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews dentro do gallery showcase.
