# ProfileAvatarWizard

Configuração de avatar em **3 steps de dados + tela de sucesso**, com 2 origens (URL e Iniciais) e preview ao vivo.

- **ID:** `profile.avatar`
- **Categoria:** `profile`
- **Módulo:** `flet_wizards.profile.avatar`
- **Importação pública:** `from flet_wizards import ProfileAvatarWizard`

---

## Descrição

Permite ao usuário escolher entre 2 origens de avatar:

- **URL** — campo URL + preview circular ao vivo via `ft.Image(src=url, fit=ft.BoxFit.COVER)`.
- **Iniciais** — campo iniciais (max 2 chars, uppercase) + 6 swatches de cor de fundo.

A tela de configuração (step 1) é **dinâmica**: o conteúdo muda conforme `state.source`. O step 2 mostra um preview circular grande (128px) do avatar final.

A origem "Arquivo" foi removida em 0.2.1 — para upload real, monte um `ft.FilePicker` no overlay do `page` e use o callback para gerar uma URL (data URL ou hospedada) que é então passada como `state.url`.

---

## Quando usar

- Onboarding inicial pedindo ao usuário para configurar foto de perfil.
- Tela de edição de avatar dentro de configurações.
- Fallback quando o usuário ainda não fez upload real (gera avatar de iniciais).

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **Origem** | 2 chips com ícone: 🔗 URL, ✏️ Iniciais. |
| 1 | **Configurar** | Painel dinâmico baseado em `state.source` (`_PanelURL` ou `_PanelIniciais`). |
| 2 | **Confirmar** | Preview circular (128px) + label da origem. |
| 3 | **Sucesso** | "Avatar salvo." + botão "Voltar ao início". |

---

## Campos por step

### Step 0 — Origem

| Campo | Tipo | UI |
|---|---|---|
| `source` | `str` | 2 `GestureDetector` chips: `"URL"`, `"Iniciais"` |

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

#### `source` vazio

Renderiza "Volte ao step anterior e selecione uma origem." (não deveria acontecer no fluxo normal — o usuário precisa passar pelo step 0).

### Step 2 — Confirmar

Preview circular (128px) via `_avatar_circle(state, 128)`:

- **Iniciais** → círculo bgcolor `state.bg_color or state.accent()`, texto branco com as iniciais. Quando `bg_color` está vazio, o círculo herda o `accent` do tema ativo.
- **URL** → `ft.Image(src=url, fit=BoxFit.COVER)` com `clip_behavior=ANTI_ALIAS`.
- Sem source/value → círculo cinza com "?".

### Step 3 — Sucesso

Check (72px) + "Avatar salvo." + botão "Voltar ao início" → `state.reset()`.

---

## Campos coletados

| Campo | Tipo | Descrição |
|---|---|---|
| `source` | `str` | `"URL"` ou `"Iniciais"`. |
| `url` | `str` | Preenchido apenas se `source == "URL"`. |
| `initials` | `str` | Até 2 caracteres, uppercase. Preenchido apenas se `source == "Iniciais"`. |
| `bg_color` | `str` | Hex da cor de fundo (apenas para iniciais). Pode ficar vazio — fallback para `state.accent()`. |

---

## Parâmetros

| Parâmetro | Tipo | Default | Descrição |
|---|---|---|---|
| `theme` | `WizardTheme` | `WizardTheme.SLATE` | Paleta visual. |
| `on_complete` | `Callable[[dict], Any] \| None` | `None` | Callback recebendo `{"source": str, "value": str}`. |
| `mock` | `bool` | `False` | Preview no gallery — inicializa com `PROFILE_AVATAR`. |

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

Schema declarado em `META.on_complete_schema = {"source": "'Iniciais'|'URL'", "value": "str"}`.

---

## Limitações conhecidas

- **Sem upload real de arquivo.** A origem "Arquivo" foi removida em 0.2.1. Para upload real, integre um `ft.FilePicker` externamente e passe a URL/path resultante via outro fluxo.
- **Sem validação de URL.** Qualquer string é aceita no campo URL — `ft.Image` simplesmente falha silenciosamente se a URL não resolver.
- **Sem validação de tamanho de iniciais.** O slice limita a 2 chars, mas 1 char (ou caractere especial) é aceito sem aviso.

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import ProfileAvatarWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_avatar(data: dict) -> None:
        # data == {"source": "Iniciais"|"URL", "value": "..."}
        if data["source"] == "URL":
            url = data["value"]
            # persistir url no perfil...
        else:
            initials = data["value"]
            # gerar avatar de iniciais server-side ou armazenar a string...

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
    "bg_color": "",
}
```

Em modo mock o wizard abre no step 2 (Confirmar) com preview circular usando `state.accent()` do tema ativo (porque `bg_color=""`) e iniciais "AL". Trocar o tema externamente repinta o círculo automaticamente.
