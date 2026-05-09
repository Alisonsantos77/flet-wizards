<!-- generated-from-hash: 228332a1e13d3ccf -->

# Recuperar Senha

> Wizard de recuperação de senha com código de verificação.

## Steps

| # | Nome          |
|---|---------------|
| 1 | E-mail       |
| 2 | Código       |
| 3 | Nova senha   |

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
from wizards.auth.recovery import RecuperarSenha

def on_complete(data):
    print(f"Senha recuperada para o e-mail: {data['email']}")

wizard = RecuperarSenha(theme='dark', on_complete=on_complete)
```

## Mock no gallery

O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews.
