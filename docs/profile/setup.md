<!-- generated-from-hash: 6a72a65b1afeb12d -->

# Setup de Perfil

> Wizard de onboarding com identidade, interesses e preferências.

## Steps

| #  | Nome          |
|----|---------------|
| 1  | Identidade    |
| 2  | Sobre         |
| 3  | Preferências   |

## Plataformas suportadas

- Windows
- macOS
- Linux
- Android
- iOS

## Retorno do `on_complete`

| Campo      | Tipo  |
|------------|-------|
| name       | str   |
| username   | str   |
| bio        | str   |
| interests  | list  |
| theme      | str   |
| language   | str   |

## Uso

```python
from wizards.profile.setup import SetupDePerfil

def on_complete(data):
    print(data)

wizard = SetupDePerfil(theme='dark', on_complete=on_complete)
```

## Mock no gallery

O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews.
