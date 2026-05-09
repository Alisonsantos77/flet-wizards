<!-- generated-from-hash: 451c4f981d96dc19 -->

# Avatar

> Wizard de configuração de avatar com 3 origens (arquivo, URL, iniciais).

## Steps

| # | Nome       |
|---|------------|
| 1 | Origem     |
| 2 | Configurar |
| 3 | Confirmar  |

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
from wizards.profile.avatar import Avatar

def on_complete(data):
    print(f"Fonte: {data['source']}, Valor: {data['value']}")

wizard = Avatar(theme="dark", on_complete=on_complete)
```

## Mock no gallery

O wizard expõe `mock=True` para abrir já no último step de dados com valores fictícios — útil em previews.
