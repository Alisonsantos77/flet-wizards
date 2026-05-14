"""ProfileSetupWizard — onboarding de perfil em 3 steps.

Steps:
  0 — Identidade: nome + username
  1 — Sobre: bio (multiline) + 6 chips de interesse (multi-select)
  2 — Preferências: 4 swatches de tema com troca ao vivo + dropdown de idioma
  3 — Sucesso

State: name, username, bio, interests (list[str]), theme_key, language.
`on_complete` recebe o dict completo, com `theme` derivado de `theme_key`.

Diferença vs auth wizards: aqui o **state.theme_key é a fonte de verdade**
do tema visual. Trocar swatch em step 2 atualiza state.theme imediatamente
(live preview). Por isso o sync `state.theme = theme` (do prop) não é
aplicado após o mount inicial — caso contrário o prop sobrescreveria a
escolha do usuário.

`mock=True` inicializa com `PROFILE_SETUP` e abre no step 2 (Preferências).
"""

import inspect
from dataclasses import dataclass, field
from typing import Awaitable, Callable, ClassVar

import flet as ft
from loguru import logger

from flet_wizards.core import (
    BaseWizardState,
    THEMES_BY_NAME,
    WizardFrame,
    WizardMeta,
    WizardTheme,
    form_field,
    primary_button,
    register,
)
from flet_wizards.core.mock_data import PROFILE_SETUP

META = register(
    WizardMeta(
        id="profile.setup",
        name="Setup de Perfil",
        category="profile",
        description="Wizard de onboarding com identidade, interesses e preferências.",
        steps=["Identidade", "Sobre", "Preferências"],
        platforms=[
            ft.PagePlatform.WINDOWS,
            ft.PagePlatform.MACOS,
            ft.PagePlatform.LINUX,
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
        ],
        on_complete_schema={
            "name": "str",
            "username": "str",
            "bio": "str",
            "interests": "list",
            "theme": "str",
            "language": "str",
        },
    )
)

INTERESTS: list[str] = ["Python", "DevOps", "Design", "AI", "Data", "Mobile"]
LANGUAGES: list[tuple[str, str]] = [
    ("pt-BR", "Português (BR)"),
    ("en-US", "English (US)"),
    ("es-ES", "Español"),
    ("fr-FR", "Français"),
]

SETUP_THEMES: list[tuple[str, WizardTheme]] = [
    ("Slate", WizardTheme.SLATE),
    ("Rose", WizardTheme.ROSE),
    ("Amber", WizardTheme.AMBER),
    ("Frost", WizardTheme.FROST),
]


def _key_for_theme(t: WizardTheme) -> str:
    """Mapeia uma instância de WizardTheme de volta para sua chave."""
    for name, theme in THEMES_BY_NAME.items():
        if theme is t:
            return name
    return "Slate"


@ft.observable
@dataclass
class ProfileSetupState(BaseWizardState):
    """Store reativo do ProfileSetupWizard."""

    TOTAL_STEPS: ClassVar[int] = 3

    name: str = ""
    username: str = ""
    bio: str = ""
    interests: list[str] = field(default_factory=list)
    theme_key: str = "Slate"
    language: str = "pt-BR"

    def reset(self) -> None:
        super().reset()
        self.name = ""
        self.username = ""
        self.bio = ""
        self.interests = []
        self.theme_key = "Slate"
        self.language = "pt-BR"


@ft.component
def StepIdentidade(state: ProfileSetupState) -> ft.Control:
    """Nome e username — primeiros dados do perfil."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    name_v, set_name = ft.use_state(state.name)
    user_v, set_user = ft.use_state(state.username)

    def on_name(e):
        set_name(e.control.value)
        state.name = e.control.value

    def on_user(e):
        set_user(e.control.value)
        state.username = e.control.value

    shared = dict(primary=P, text=T, sub=S, card=C, border=B)

    return ft.Column(
        [
            ft.Text(
                "Quem é você?",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Informe seu nome e o nome de usuário público.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            form_field("NOME", name_v, on_name, "Nome completo", **shared),
            ft.Container(height=18),
            form_field(
                "USERNAME",
                user_v,
                on_user,
                "ada.lovelace",
                **shared,
            ),
        ],
        spacing=0,
    )


@ft.component
def StepSobre(state: ProfileSetupState) -> ft.Control:
    """Bio multiline + chips de interesse multi-select."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    bio_v, set_bio = ft.use_state(state.bio)
    interests_v, set_interests = ft.use_state(state.interests)

    def on_bio(e):
        set_bio(e.control.value)
        state.bio = e.control.value

    def toggle(label: str):
        new_list = (
            [i for i in interests_v if i != label]
            if label in interests_v
            else interests_v + [label]
        )
        set_interests(new_list)
        state.interests = new_list

    def chip(label: str) -> ft.GestureDetector:
        sel = label in interests_v
        return ft.GestureDetector(
            on_tap=lambda _e, l=label: toggle(l),
            content=ft.Container(
                content=ft.Text(
                    label,
                    size=12,
                    color="#FFFFFF" if sel else S,
                    weight=ft.FontWeight.W_600 if sel else ft.FontWeight.W_400,
                ),
                bgcolor=P if sel else C,
                padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                border_radius=20,
                border=ft.Border.all(1, P if sel else B),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
            ),
        )

    chip_rows = [INTERESTS[:3], INTERESTS[3:]]
    shared = dict(primary=P, text=T, sub=S, card=C, border=B)

    return ft.Column(
        [
            ft.Text(
                "Sobre você",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Escreva uma bio curta e selecione seus interesses.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            form_field(
                "BIO",
                bio_v,
                on_bio,
                "Conte um pouco sobre você",
                multiline=True,
                **shared,
            ),
            ft.Container(height=22),
            ft.Text(
                "INTERESSES",
                size=11,
                color=S,
                weight=ft.FontWeight.W_500,
                style=ft.TextStyle(letter_spacing=0.8),
            ),
            ft.Container(height=10),
            *[
                ft.Column(
                    [
                        ft.Row([chip(i) for i in row], spacing=8),
                        ft.Container(height=8),
                    ],
                    spacing=0,
                )
                for row in chip_rows
            ],
        ],
        spacing=0,
    )


@ft.component
def StepPreferencias(state: ProfileSetupState) -> ft.Control:
    """4 swatches de tema (live preview) + dropdown de idioma."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    lang_v, set_lang = ft.use_state(state.language)

    def pick_theme(name: str, theme: WizardTheme):
        state.theme_key = name
        state.theme = theme

    def on_lang(e):
        set_lang(e.control.value)
        state.language = e.control.value

    def theme_swatch(name: str, theme: WizardTheme) -> ft.GestureDetector:
        sel = state.theme_key == name
        return ft.GestureDetector(
            on_tap=lambda _e, n=name, t=theme: pick_theme(n, t),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            width=64,
                            height=40,
                            bgcolor=theme.surface,
                            border_radius=6,
                            content=ft.Row(
                                [
                                    ft.Container(
                                        width=8,
                                        height=8,
                                        bgcolor=theme.primary,
                                        border_radius=4,
                                    ),
                                    ft.Container(
                                        width=8,
                                        height=8,
                                        bgcolor=theme.secondary,
                                        border_radius=4,
                                    ),
                                    ft.Container(
                                        width=8,
                                        height=8,
                                        bgcolor=theme.accent,
                                        border_radius=4,
                                    ),
                                ],
                                spacing=4,
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            name,
                            size=11,
                            color=T,
                            weight=ft.FontWeight.W_600
                            if sel
                            else ft.FontWeight.W_400,
                        ),
                    ],
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=C,
                padding=ft.Padding.all(10),
                border_radius=8,
                border=ft.Border.all(2 if sel else 1, P if sel else B),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
            ),
        )

    return ft.Column(
        [
            ft.Text(
                "Personalize",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Escolha um tema e o idioma da interface.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            ft.Text(
                "TEMA",
                size=11,
                color=S,
                weight=ft.FontWeight.W_500,
                style=ft.TextStyle(letter_spacing=0.8),
            ),
            ft.Container(height=10),
            ft.Row(
                [theme_swatch(name, theme) for name, theme in SETUP_THEMES],
                spacing=10,
            ),
            ft.Container(height=22),
            ft.Text(
                "IDIOMA",
                size=11,
                color=S,
                weight=ft.FontWeight.W_500,
                style=ft.TextStyle(letter_spacing=0.8),
            ),
            ft.Container(height=10),
            ft.Dropdown(
                value=lang_v,
                options=[
                    ft.DropdownOption(key=k, text=label)
                    for k, label in LANGUAGES
                ],
                on_select=on_lang,
                border_color=B,
                bgcolor=C,
                color=T,
                border_radius=8,
                text_size=14,
                width=260,
            ),
        ],
        spacing=0,
    )


@ft.component
def StepSuccess(state: ProfileSetupState) -> ft.Control:
    """Tela final — confirmação visual e botão de reset."""

    P = state.primary()
    T = state.text()
    S = state.sub()

    check = ft.Container(
        width=72,
        height=72,
        border_radius=36,
        bgcolor=P,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            "✓",
            size=36,
            color="#FFFFFF",
            weight=ft.FontWeight.BOLD,
        ),
    )

    return ft.Column(
        [
            ft.Container(expand=1),
            ft.Column(
                [
                    check,
                    ft.Container(height=24),
                    ft.Text(
                        f"Perfil pronto, {state.name.split()[0] if state.name else 'visitante'}.",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=T,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Suas preferências foram salvas.",
                        size=13,
                        color=S,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=28),
                    primary_button(
                        "Recomeçar",
                        lambda _: state.reset(),
                        P,
                        mode=state.theme.mode,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
            ft.Container(expand=1),
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )


CompleteCallback = Callable[[dict], "None | Awaitable[None]"]


@ft.component
def ProfileSetupWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: CompleteCallback | None = None,
    mock: bool = False,
) -> ft.Control:
    """Wizard público de setup de perfil — 3 steps + sucesso.

    `mock=True` (modo gallery) inicializa com `PROFILE_SETUP` e abre no
    último step de dados (Preferências). O state.theme_key controla o
    tema visual; o prop `theme` é apenas a aparência inicial quando não
    em modo mock.
    """

    if mock:
        key = PROFILE_SETUP["theme_key"]
        initial = ProfileSetupState(
            theme=THEMES_BY_NAME.get(key, theme),
            step=ProfileSetupState.TOTAL_STEPS - 1,
            **PROFILE_SETUP,
        )
    else:
        initial = ProfileSetupState(
            theme=theme,
            theme_key=_key_for_theme(theme),
        )

    state, _ = ft.use_state(initial)

    async def _adapt(s: ProfileSetupState) -> None:
        if on_complete is None:
            logger.warning(
                "[ProfileSetupWizard]: on_complete não fornecido — wizard funcionará como demo"
            )
            return
        result = on_complete(
            {
                "name": s.name,
                "username": s.username,
                "bio": s.bio,
                "interests": list(s.interests),
                "theme": s.theme_key,
                "language": s.language,
            }
        )
        if inspect.isawaitable(result):
            await result

    return WizardFrame(
        state=state,
        step_labels=["Identidade", "Sobre", "Preferências"],
        step_hints=["Nome e usuário", "Bio e interesses", "Tema e idioma"],
        steps=[StepIdentidade, StepSobre, StepPreferencias, StepSuccess],
        on_complete=_adapt,
        last_step_label="Salvar perfil",
        loading_label="Salvando...",
    )
