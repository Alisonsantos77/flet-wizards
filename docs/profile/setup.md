# ProfileSetupWizard

Onboarding de perfil em **3 steps de dados + tela de sucesso**, com seleção de tema ao vivo.

- **ID:** `profile.setup`
- **Categoria:** `profile`
- **Módulo:** `flet_wizards.profile.setup`
- **Importação pública:** `from flet_wizards import ProfileSetupWizard`

---

## Descrição

Coleta identidade (nome + username), bio + interesses (multi-select) e preferências (tema + idioma). O step 2 troca o tema visual do próprio wizard ao vivo: clicar em um swatch atualiza `state.theme_key` **e** `state.theme`, repintando a UI imediatamente.

Diferença vs auth wizards: aqui o **`state.theme_key` é a fonte de verdade** do tema. Por isso o sync `state.theme = theme` (do prop) **não é aplicado após o mount inicial** — caso contrário o prop sobrescreveria a escolha do usuário a cada re-render.

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **Identidade** | Nome + username. |
| 1 | **Sobre** | Bio multiline + 6 chips de interesse multi-select. |
| 2 | **Preferências** | 4 swatches de tema (live preview) + dropdown de idioma. |
| 3 | **Sucesso** | "Perfil pronto, {primeiro nome}." + botão "Recomeçar". |

---

## Campos por step

### Step 0 — Identidade

| Campo | Tipo | UI |
|---|---|---|
| `name` | `str` | `form_field("NOME", ..., "Nome completo")` |
| `username` | `str` | `form_field("USERNAME", ..., "ada.lovelace")` |

### Step 1 — Sobre

| Campo | Tipo | UI |
|---|---|---|
| `bio` | `str` | `form_field("BIO", ..., multiline=True)` |
| `interests` | `list[str]` | 6 chips multi-select: `Python`, `DevOps`, `Design`, `AI`, `Data`, `Mobile` |

### Step 2 — Preferências

| Campo | Tipo | UI |
|---|---|---|
| `theme_key` | `str` | 4 swatches: `Slate`, `Rose`, `Amber`, `Frost` (preview com 3 dots: primary/secondary/accent) |
| `language` | `str` | `ft.Dropdown` com `on_select` (não `on_change` no Flet 0.85+) |

Idiomas disponíveis: `pt-BR`, `en-US`, `es-ES`, `fr-FR`.

Trocar swatch chama `pick_theme(name)` que faz **dois** updates no state:

```python
state.theme_key = name
state.theme = THEMES_BY_NAME[name]
```

A reatividade do `@ft.observable` propaga a mudança para todos os componentes filhos.

### Step 3 — Sucesso

Check (72px) + "Perfil pronto, {primeiro nome}." + botão "Recomeçar" → `state.reset()`.

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
{
    "name": str,
    "username": str,
    "bio": str,
    "interests": list,   # list[str]
    "theme": str,        # chave: "Slate" | "Rose" | "Amber" | "Frost" (ou outro registrado em THEMES_BY_NAME)
    "language": str,     # ex.: "pt-BR"
}
```

Schema declarado em `META.on_complete_schema`. O campo `theme` no payload é a string `theme_key` — consumidores podem reconstruir a paleta via `THEMES_BY_NAME[theme]`.

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import ProfileSetupWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_setup(data: dict) -> None:
        # data == {"name": ..., "username": ..., "bio": ...,
        #          "interests": [...], "theme": "Slate", "language": "pt-BR"}
        ...

    return ProfileSetupWizard(
        theme=WizardTheme.SLATE,
        on_complete=handle_setup,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.bgcolor = "#0B0B0F"
    page.render(App)


ft.run(main)
```

---

## Mock no gallery

`flet_wizards.core.mock_data.PROFILE_SETUP`:

```python
PROFILE_SETUP = {
    "name": "Ada Lovelace",
    "username": "ada.lovelace",
    "bio": "Engenheira de software apaixonada por sistemas distribuídos.",
    "interests": ["Python", "DevOps"],
    "theme_key": "Slate",
    "language": "pt-BR",
}
```

Em modo mock o wizard abre no step 2 (Preferências) com Slate selecionado e idioma `pt-BR`. Trocar de swatch repinta o wizard inteiro ao vivo.

> O seletor expõe 4 swatches (`Slate`, `Rose`, `Amber`, `Frost`) por padrão para evitar fadiga visual. Os outros temas registrados em `THEMES_BY_NAME` (Emerald, Azure, Crimson) continuam disponíveis via `WizardTheme.X` direto — apenas não aparecem no seletor enxuto.
