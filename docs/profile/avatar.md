# ProfileAvatarWizard

Configuração de avatar em **3 steps de dados + tela de sucesso**, com 3 origens (arquivo, URL, iniciais) e preview ao vivo.

- **ID:** `profile.avatar`
- **Categoria:** `profile`
- **Módulo:** `flet_wizards.profile.avatar`
- **Importação pública:** `from flet_wizards import ProfileAvatarWizard`

---

## Descrição

Permite ao usuário escolher entre 3 origens de avatar:

- **Arquivo** — botão de seleção (placeholder; integração com `ft.FilePicker` real exige overlay no `page` e fica a cargo do consumidor).
- **URL** — campo URL + preview circular ao vivo via `ft.Image(src=url, fit=ft.BoxFit.COVER)`.
- **Iniciais** — campo iniciais (max 2 chars, uppercase) + 6 swatches de cor de fundo.

A tela de configuração (step 1) é **dinâmica**: o conteúdo muda conforme `state.source`. O step 2 mostra um preview circular grande (128px) do avatar final.

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **Origem** | 3 chips com ícone: 📁 Arquivo, 🔗 URL, ✏️ Iniciais. |
| 1 | **Configurar** | Painel dinâmico baseado em `state.source` (`_PanelArquivo`, `_PanelURL` ou `_PanelIniciais`). |
| 2 | **Confirmar** | Preview circular (128px) + label da origem. |
| 3 | **Sucesso** | "Avatar salvo." + botão "Voltar ao início". |

---

## Campos por step

### Step 0 — Origem

| Campo | Tipo | UI |
|---|---|---|
| `source` | `str` | 3 `GestureDetector` chips: `"Arquivo"`, `"URL"`, `"Iniciais"` |

### Step 1 — Configurar

Renderização baseada em `state.source`:

#### `source == "Iniciais"` → `_PanelIniciais`

| Campo | Tipo | UI |
|---|---|---|
| `initials` | `str` | `form_field("INICIAIS", ..., "AB")` — limita a 2 chars uppercase via `(value or "")[:2].upper()` |
| `bg_color` | `str` | 6 swatches circulares (32px): `#7C6EF6`, `#34D399`, `#F472B6`, `#60A5FA`, `#FB923C`, `#A78BFA` |

#### `source == "URL"` → `_PanelURL`

| Campo | Tipo | UI |
|---|---|---|
| `url` | `str` | `form_field("URL DA IMAGEM", ..., "https://...")` |

Mais um preview circular (96px) embaixo, atualizado ao vivo.

#### `source == "Arquivo"` → `_PanelArquivo`

Botão ghost "Escolher arquivo" (stub que seta `state.file_path = "storage/temp/avatar_demo.png"`). Para o file picker real, monte um `ft.FilePicker` no overlay do `page` e atualize `state.file_path` no callback de seleção.

#### `source` vazio

Renderiza "Volte ao step anterior e selecione uma origem." (não deveria acontecer no fluxo normal porque o usuário precisa passar pelo step 0).

### Step 2 — Confirmar

Preview circular (128px) via `_avatar_circle(state, 128)`:

- Iniciais → círculo bgcolor `bg_color`, texto branco com as iniciais.
- URL → `ft.Image(src=url, fit=BoxFit.COVER)` com `clip_behavior=ANTI_ALIAS`.
- Arquivo → mesmo que URL, com `src=file_path`.
- Sem source/value → círculo cinza com "?".

### Step 3 — Sucesso

Check (72px) + "Avatar salvo." + botão "Voltar ao início" → `state.reset()`.

---

## Plataformas suportadas

```python
[
    ft.PagePlatform.WINDOWS,
    ft.PagePlatform.MACOS,
    ft.PagePlatform.LINUX,
    ft.PagePlatform.ANDROID,
    ft.PagePlatform.IOS,
]
```

---

## Retorno do `on_complete`

```python
{"source": str, "value": str}
```

`value` é resolvido via `_value_from_state(state)`:

| `state.source` | `value` |
|---|---|
| `"Iniciais"` | `state.initials` |
| `"URL"` | `state.url` |
| `"Arquivo"` | `state.file_path` |

Schema declarado em `META.on_complete_schema = {"source": "str", "value": "str"}`.

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import ProfileAvatarWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_avatar(data: dict) -> None:
        # data == {"source": "Iniciais"|"URL"|"Arquivo", "value": "..."}
        if data["source"] == "URL":
            url = data["value"]
            ...

    return ProfileAvatarWizard(
        theme=WizardTheme.ROSE,
        on_complete=handle_avatar,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.bgcolor = "#0B0B0F"
    page.render(App)


ft.run(main)
```

---

## Mock no gallery

`flet_wizards.core.mock_data.PROFILE_AVATAR`:

```python
PROFILE_AVATAR = {
    "source": "Iniciais",
    "initials": "AL",
    "bg_color": "#7C6EF6",
}
```

Em modo mock o wizard abre no step 2 (Confirmar) já mostrando o preview circular roxo com "AL". Os campos `url` e `file_path` ficam vazios — só "Iniciais" é demonstrado no preview.
