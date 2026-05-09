<!-- generated-from-hash: 0af370786c8bccf7 -->

# Cadastro

> Wizard de cadastro com conta, perfil e confirmação.

## Steps

| #  | Nome      |
|----|-----------|
| 1  | Conta     |
| 2  | Perfil    |
| 3  | Confirmar |

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
from wizards.auth.auth import Cadastro

def on_complete(data):
    print(f"Email: {data['email']}, Nome: {data['name']}, Papel: {data['role']}")

wizard = Cadastro(theme="dark", on_complete=on_complete)
```

## Mock no gallery

O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews.
