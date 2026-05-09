<!-- generated-from-hash: f0bf5b6c241f0f5c -->

# Editar Perfil

> Wizard de edição de perfil com diff visual no resumo.

## Steps

| #  | Nome       |
|----|------------|
| 1  | Dados      |
| 2  | Segurança  |
| 3  | Confirmar  |

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
from wizards.profile.edit import EditarPerfil

def on_complete(data):
    print("Campos alterados:", data['changed_fields'])

wizard = EditarPerfil(theme='dark', on_complete=on_complete)
```

## Mock no gallery

O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews.
