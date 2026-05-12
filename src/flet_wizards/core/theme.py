"""Sistema de temas dos flet_wizards.

Define `WizardTheme` como dataclass imutável com a paleta completa exigida
por todos os componentes (`primary`, `secondary`, `accent`, `bg`, `surface`,
`card`, `panel`, `border`, `text`, `sub`) e um campo `mode` indicando se a
paleta foi desenhada para light ou dark mode.

Built-ins (`SLATE`, `EMERALD`, `ROSE`, `AZURE`, `FOREST`, `CRIMSON`, `FROST`)
são instâncias anexadas à própria classe. `THEMES_BY_NAME` expõe o mesmo
conjunto indexado pelo nome capitalizado, útil para seletores baseados em
string.
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


WizardTheme.SLATE = WizardTheme(
    primary="#7C6EF6",
    secondary="#A89EFA",
    accent="#38BDF8",
    bg="#0B0B0F",
    surface="#111118",
    card="#17171F",
    panel="#141420",
    border="#222230",
    text="#F0EEF8",
    sub="#6B6880",
)

WizardTheme.EMERALD = WizardTheme(
    primary="#34D399",
    secondary="#6EE7B7",
    accent="#60A5FA",
    bg="#090E0C",
    surface="#0E1610",
    card="#121C14",
    panel="#101810",
    border="#1C2E1E",
    text="#ECFDF5",
    sub="#4A7060",
)

WizardTheme.ROSE = WizardTheme(
    primary="#F472B6",
    secondary="#FBCFE8",
    accent="#FB923C",
    bg="#0E090C",
    surface="#170E12",
    card="#1C1016",
    panel="#180E14",
    border="#2C1820",
    text="#FDF2F8",
    sub="#7A3C58",
)

WizardTheme.AZURE = WizardTheme(
    primary="#60A5FA",
    secondary="#93C5FD",
    accent="#A78BFA",
    bg="#080B10",
    surface="#0D1018",
    card="#12161E",
    panel="#0F1420",
    border="#1C2236",
    text="#EFF6FF",
    sub="#3C5070",
)

WizardTheme.FOREST = WizardTheme(
    primary="#4ADE80",
    secondary="#86EFAC",
    accent="#22C55E",
    bg="#071A09",
    surface="#0D1F0F",
    card="#1A3D1E",
    panel="#091409",
    border="#2D5C33",
    text="#FFFFFF",
    sub="#B8D4BB",
    mode=ft.ThemeMode.DARK,
)

WizardTheme.CRIMSON = WizardTheme(
    primary="#DE1F26",
    secondary="#FF4444",
    accent="#FF6B6B",
    bg="#0D0D0D",
    surface="#141414",
    card="#1A1A1A",
    panel="#111111",
    border="#2A2A2A",
    text="#F5F5F5",
    sub="#999999",
    mode=ft.ThemeMode.DARK,
)

WizardTheme.FROST = WizardTheme(
    primary="#0052FF",
    secondary="#3B82F6",
    accent="#60A5FA",
    bg="#F8FAFC",
    surface="#FFFFFF",
    card="#F1F5F9",
    panel="#E2E8F0",
    border="#CBD5E1",
    text="#0F172A",
    sub="#64748B",
    mode=ft.ThemeMode.LIGHT,
)


THEMES_BY_NAME: dict[str, WizardTheme] = {
    "Slate": WizardTheme.SLATE,
    "Emerald": WizardTheme.EMERALD,
    "Rose": WizardTheme.ROSE,
    "Azure": WizardTheme.AZURE,
    "Forest": WizardTheme.FOREST,
    "Crimson": WizardTheme.CRIMSON,
    "Frost": WizardTheme.FROST,
}


DEFAULT_THEME: WizardTheme = WizardTheme.SLATE
