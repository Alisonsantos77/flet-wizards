<!-- generated-from-hash: 9dd98340c63ea86c -->

# Login Clássico

> Wizard de login com e-mail e senha em dois steps.

## Steps

| #  | Nome           |
|----|----------------|
| 1  | Acesso         |
| 2  | Confirmação    |

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
from wizards.auth.login import LoginClassico

def on_complete(data):
    print(f"E-mail: {data['email']}")

wizard = LoginClassico(theme='dark', on_complete=on_complete)
```

## Mock no gallery

O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews.
