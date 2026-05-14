# Sistema de temas

A lib expõe 7 pares de temas, cada um em duas variantes (dark e light), totalizando 14 paletas internas. O dev escolhe pelo nome do par; a variante é selecionada explicitamente (`WizardTheme.SLATE` vs `WizardTheme.SLATE_LIGHT`) ou via `resolve_theme(theme, mode)`.

---

## Pares disponíveis

| Par | Atributo dark | Atributo light | Dark primary | Light primary |
|---|---|---|---|---|
| Slate | `WizardTheme.SLATE` | `WizardTheme.SLATE_LIGHT` | `#7C6EF6` | `#6366F1` |
| Emerald | `WizardTheme.EMERALD` | `WizardTheme.EMERALD_LIGHT` | `#6EE7B7` | `#059669` |
| Rose | `WizardTheme.ROSE` | `WizardTheme.ROSE_LIGHT` | `#FB7185` | `#E11D48` |
| Azure | `WizardTheme.AZURE` | `WizardTheme.AZURE_LIGHT` | `#818CF8` | `#4F46E5` |
| Amber | `WizardTheme.AMBER` | `WizardTheme.AMBER_LIGHT` | `#F59E0B` | `#D97706` |
| Crimson | `WizardTheme.CRIMSON` | `WizardTheme.CRIMSON_LIGHT` | `#DE1F26` | `#B91C1C` |
| Frost | `WizardTheme.FROST_DARK` | `WizardTheme.FROST` | `#60A5FA` | `#0052FF` |

> **Nota sobre Frost:** o par tem nomenclatura invertida em relação aos outros. `WizardTheme.FROST` é a variante **light** (padrão histórico), enquanto `WizardTheme.FROST_DARK` é a variante dark. Os demais pares seguem `X` = dark, `X_LIGHT` = light.

---

## Tokens de cor

Cada `WizardTheme` expõe 10 tokens de cor + 2 metadados:

| Token | Uso típico |
|---|---|
| `primary` | Botões CTA, indicador de step ativo, barra de progresso. |
| `secondary` | Variações suaves de `primary`. |
| `accent` | Destaques pontuais (avatar default, hover states). |
| `bg` | Fundo da página inteira. |
| `surface` | Cards de revisão, painéis elevados. |
| `card` | Background de `TextField`, chips, swatches. |
| `panel` | Sidebar dos wizards desktop. |
| `border` | Borda neutra de cards, divisores. |
| `text` | Texto primário (alto contraste sobre `bg`). |
| `sub` | Texto secundário (hints, labels minúsculos). |
| `mode` | `ft.ThemeMode.DARK` ou `ft.ThemeMode.LIGHT`. |
| `pair_name` | Identifica o par (`"slate"`, `"emerald"`, ...) para `resolve_theme` localizar a variante oposta. |

---

## Uso direto

```python
from flet_wizards import AuthLoginWizard, WizardTheme

AuthLoginWizard(theme=WizardTheme.SLATE)        # variante dark
AuthLoginWizard(theme=WizardTheme.SLATE_LIGHT)  # variante light
AuthLoginWizard(theme=WizardTheme.AMBER)        # outra família, dark
```

---

## Detecção automática via `resolve_theme`

```python
import flet as ft
from flet_wizards import AuthLoginWizard, WizardTheme
from flet_wizards.core import resolve_theme


@ft.component
def App() -> ft.Control:
    page = ft.context.page
    theme = resolve_theme(WizardTheme.SLATE, page.theme_mode)
    return AuthLoginWizard(theme=theme)


async def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.render(App)


ft.run(main)
```

Comportamento de `resolve_theme(theme, mode)`:

| `mode` | Resultado |
|---|---|
| `ft.ThemeMode.DARK` | Variante dark do par. |
| `ft.ThemeMode.LIGHT` | Variante light do par. |
| `ft.ThemeMode.SYSTEM` | Consulta `ft.context.page.platform_brightness`. Em DARK retorna a variante dark; caso contrário (LIGHT ou indisponível), retorna a variante light. |

Se `theme.pair_name` não estiver registrado em `THEME_PAIRS` (paleta customizada criada pelo dev), `resolve_theme` devolve o próprio `theme` sem alteração — fallback seguro.

---

## Convenções de fundo em temas dark

Pares com `primary` saturado (Rose, Amber, Crimson) usam `bg`/`surface`/`card` neutros escuros (`#0D0D0D`/`#161616`/`#1C1C1C`) para que a identidade da cor fique no `primary` e `accent` sem contaminar o fundo. Isso evita aparência "tonalizada" do app inteiro e mantém identidades visuais distintas mesmo entre temas com a mesma família de bg.

Pares com `primary` mais suave (Slate, Emerald, Azure) usam `bg`/`surface`/`card` com tint da cor identidade.

Todas as 7 variantes light têm `bg=#FFFFFF`, `surface=#FFFFFF`, `card=#FAFAFA`. O tint da cor identidade é preservado apenas em `panel` (sidebar). Border padronizado em `#E2E8F0` neutro.

---

## Paletas customizadas

`WizardTheme` é uma dataclass — qualquer dev pode criar uma paleta própria:

```python
from flet_wizards import WizardTheme

MY_THEME = WizardTheme(
    primary="#FF6B35",
    secondary="#FFA07A",
    accent="#E63946",
    bg="#0A0A0A",
    surface="#141414",
    card="#1A1A1A",
    panel="#0F0F0F",
    border="#2A2A2A",
    text="#FFFFFF",
    sub="#888888",
    mode=ft.ThemeMode.DARK,
    pair_name="",  # vazio = `resolve_theme` devolve este próprio tema sem buscar par
)
```

Paletas customizadas não participam de `THEME_PAIRS` nem têm variante light automática — quem cria uma também precisa criar a contraparte se quiser suporte a `resolve_theme`.

---

## API pública relacionada

Exportadas em `flet_wizards.core`:

- `WizardTheme` — dataclass de paleta.
- `THEME_PAIRS` — `dict[str, tuple[dark, light]]` indexado por `pair_name`.
- `THEMES_BY_NAME` — `dict[str, WizardTheme]` com 7 entradas (um tema por par, capitalizado).
- `DEFAULT_THEME` — `WizardTheme.SLATE`.
- `resolve_theme(theme, mode)` — função descrita acima.
