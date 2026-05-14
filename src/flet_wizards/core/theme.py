"""Sistema de temas dos flet_wizards — pares dark/light por combinação.

Cada combinação de tema (slate, emerald, rose, azure, amber, crimson, frost)
existe em duas variantes: dark e light. As 14 paletas são anexadas como
atributos da classe (`WizardTheme.SLATE`, `WizardTheme.SLATE_LIGHT`, etc.)
e indexadas por `pair_name` em `THEME_PAIRS`, permitindo encontrar a
variante oposta dado um tema ativo.

Use `resolve_theme(theme, mode)` para selecionar a variante correta a partir
de um `ft.ThemeMode` (DARK / LIGHT / SYSTEM). Em SYSTEM, consulta
`ft.context.page.platform_brightness` quando disponível e cai em DARK como
default seguro fora de contexto reativo.

`THEMES_BY_NAME` continua expondo 7 entradas (uma por par, com o nome
capitalizado) para compatibilidade com código que ainda escolhe tema por
string — mantém o comportamento atual (SLATE/EMERALD/ROSE/AZURE/AMBER/
CRIMSON dark + FROST light).

Convenção de bg em temas dark de alta saturação: paletas cujo `primary`
é uma cor saturada (Rose, Amber) usam bg/panel/surface/card neutros
escuros para que a identidade da cor fique no `primary` e `accent` sem
contaminar o fundo, evitando aparência "tonalizada" do app inteiro.
"""

from dataclasses import dataclass

import flet as ft


@dataclass(frozen=True)
class WizardTheme:
    """Paleta de cores aplicada a um wizard."""

    primary: str
    secondary: str
    accent: str
    bg: str
    surface: str
    card: str
    panel: str
    border: str
    text: str
    sub: str
    mode: ft.ThemeMode = ft.ThemeMode.DARK
    pair_name: str = ""


WizardTheme.SLATE = WizardTheme(
    primary="#7C6EF6",
    secondary="#A78BFA",
    accent="#6D28D9",
    bg="#0B0B0F",
    surface="#111118",
    card="#16161F",
    panel="#0D0D14",
    border="#1E1E2E",
    text="#F8F8FF",
    sub="#6B7280",
    mode=ft.ThemeMode.DARK,
    pair_name="slate",
)

WizardTheme.SLATE_LIGHT = WizardTheme(
    primary="#6366F1",
    secondary="#818CF8",
    accent="#4F46E5",
    bg="#FFFFFF",
    surface="#FFFFFF",
    card="#FAFAFA",
    panel="#F5F3FF",
    border="#E2E8F0",
    text="#1E1B4B",
    sub="#6D6D8A",
    mode=ft.ThemeMode.LIGHT,
    pair_name="slate",
)

WizardTheme.EMERALD = WizardTheme(
    primary="#6EE7B7",
    secondary="#A7F3D0",
    accent="#34D399",
    bg="#0C1210",
    surface="#111F19",
    card="#162B20",
    panel="#0E1612",
    border="#1E3D2A",
    text="#F0FDF4",
    sub="#6B8F76",
    mode=ft.ThemeMode.DARK,
    pair_name="emerald",
)

WizardTheme.EMERALD_LIGHT = WizardTheme(
    primary="#059669",
    secondary="#10B981",
    accent="#047857",
    bg="#FFFFFF",
    surface="#FFFFFF",
    card="#FAFAFA",
    panel="#F0FDF9",
    border="#E2E8F0",
    text="#052E16",
    sub="#166534",
    mode=ft.ThemeMode.LIGHT,
    pair_name="emerald",
)

WizardTheme.ROSE = WizardTheme(
    primary="#FB7185",
    secondary="#FDA4AF",
    accent="#F43F5E",
    bg="#0D0D0D",
    surface="#161616",
    card="#1C1C1C",
    panel="#111111",
    border="#2A2A2A",
    text="#FFF1F2",
    sub="#9F5060",
    mode=ft.ThemeMode.DARK,
    pair_name="rose",
)

WizardTheme.ROSE_LIGHT = WizardTheme(
    primary="#E11D48",
    secondary="#FB7185",
    accent="#BE123C",
    bg="#FFFFFF",
    surface="#FFFFFF",
    card="#FAFAFA",
    panel="#FFF1F2",
    border="#E2E8F0",
    text="#4C0519",
    sub="#9F1239",
    mode=ft.ThemeMode.LIGHT,
    pair_name="rose",
)

WizardTheme.AZURE = WizardTheme(
    primary="#818CF8",
    secondary="#A5B4FC",
    accent="#6366F1",
    bg="#080C18",
    surface="#0F1628",
    card="#141D35",
    panel="#0A0F1E",
    border="#1E2D52",
    text="#EEF2FF",
    sub="#6272A4",
    mode=ft.ThemeMode.DARK,
    pair_name="azure",
)

WizardTheme.AZURE_LIGHT = WizardTheme(
    primary="#4F46E5",
    secondary="#6366F1",
    accent="#3730A3",
    bg="#FFFFFF",
    surface="#FFFFFF",
    card="#FAFAFA",
    panel="#EEF2FF",
    border="#E2E8F0",
    text="#1E1B4B",
    sub="#4338CA",
    mode=ft.ThemeMode.LIGHT,
    pair_name="azure",
)

WizardTheme.AMBER = WizardTheme(
    primary="#F59E0B",
    secondary="#FCD34D",
    accent="#D97706",
    bg="#0D0D0D",
    surface="#161616",
    card="#1C1C1C",
    panel="#111111",
    border="#2A2A2A",
    text="#FFFBEB",
    sub="#92794A",
    mode=ft.ThemeMode.DARK,
    pair_name="amber",
)

WizardTheme.AMBER_LIGHT = WizardTheme(
    primary="#D97706",
    secondary="#F59E0B",
    accent="#B45309",
    bg="#FFFFFF",
    surface="#FFFFFF",
    card="#FAFAFA",
    panel="#FFFBEB",
    border="#E2E8F0",
    text="#451A03",
    sub="#92400E",
    mode=ft.ThemeMode.LIGHT,
    pair_name="amber",
)

WizardTheme.CRIMSON = WizardTheme(
    primary="#DE1F26",
    secondary="#FF4444",
    accent="#FF6B6B",
    bg="#0D0D0D",
    surface="#161616",
    card="#1A1A1A",
    panel="#111111",
    border="#2A2A2A",
    text="#F5F5F5",
    sub="#999999",
    mode=ft.ThemeMode.DARK,
    pair_name="crimson",
)

WizardTheme.CRIMSON_LIGHT = WizardTheme(
    primary="#B91C1C",
    secondary="#DC2626",
    accent="#991B1B",
    bg="#FFFFFF",
    surface="#FFFFFF",
    card="#FAFAFA",
    panel="#FEF2F2",
    border="#E2E8F0",
    text="#450A0A",
    sub="#991B1B",
    mode=ft.ThemeMode.LIGHT,
    pair_name="crimson",
)

WizardTheme.FROST_DARK = WizardTheme(
    primary="#60A5FA",
    secondary="#93C5FD",
    accent="#3B82F6",
    bg="#0A0F1E",
    surface="#111827",
    card="#1A2540",
    panel="#0D1428",
    border="#1E3A5F",
    text="#E0F2FE",
    sub="#64748B",
    mode=ft.ThemeMode.DARK,
    pair_name="frost",
)

WizardTheme.FROST = WizardTheme(
    primary="#0052FF",
    secondary="#3B82F6",
    accent="#60A5FA",
    bg="#FFFFFF",
    surface="#FFFFFF",
    card="#FAFAFA",
    panel="#F1F5F9",
    border="#CBD5E1",
    text="#0F172A",
    sub="#64748B",
    mode=ft.ThemeMode.LIGHT,
    pair_name="frost",
)


THEME_PAIRS: dict[str, tuple[WizardTheme, WizardTheme]] = {
    "slate":   (WizardTheme.SLATE,      WizardTheme.SLATE_LIGHT),
    "emerald": (WizardTheme.EMERALD,    WizardTheme.EMERALD_LIGHT),
    "rose":    (WizardTheme.ROSE,       WizardTheme.ROSE_LIGHT),
    "azure":   (WizardTheme.AZURE,      WizardTheme.AZURE_LIGHT),
    "amber":   (WizardTheme.AMBER,      WizardTheme.AMBER_LIGHT),
    "crimson": (WizardTheme.CRIMSON,    WizardTheme.CRIMSON_LIGHT),
    "frost":   (WizardTheme.FROST_DARK, WizardTheme.FROST),
}


def resolve_theme(theme: WizardTheme, mode: ft.ThemeMode) -> WizardTheme:
    """Resolve a variante (dark/light) do par do `theme` para o `mode` pedido.

    - `DARK`  → primeiro elemento do par (variante dark).
    - `LIGHT` → segundo elemento do par (variante light).
    - `SYSTEM` → consulta `ft.context.page.platform_brightness`. Se DARK,
      retorna a variante dark; caso contrário (LIGHT ou indisponível),
      retorna a variante light.

    Se `theme.pair_name` não estiver registrado em `THEME_PAIRS`, o próprio
    `theme` é devolvido sem alteração — fallback seguro para paletas
    customizadas criadas pelo dev fora dos built-ins.
    """

    pair = THEME_PAIRS.get(theme.pair_name)
    if pair is None:
        return theme

    dark_variant, light_variant = pair

    if mode == ft.ThemeMode.DARK:
        return dark_variant
    if mode == ft.ThemeMode.LIGHT:
        return light_variant

    try:
        brightness = ft.context.page.platform_brightness
    except Exception:
        return dark_variant

    if brightness == ft.Brightness.DARK:
        return dark_variant
    return light_variant


THEMES_BY_NAME: dict[str, WizardTheme] = {
    "Slate": WizardTheme.SLATE,
    "Emerald": WizardTheme.EMERALD,
    "Rose": WizardTheme.ROSE,
    "Azure": WizardTheme.AZURE,
    "Amber": WizardTheme.AMBER,
    "Crimson": WizardTheme.CRIMSON,
    "Frost": WizardTheme.FROST,
}


DEFAULT_THEME: WizardTheme = WizardTheme.SLATE
