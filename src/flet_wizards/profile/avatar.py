"""ProfileAvatarWizard — escolha de avatar em 3 steps.

Steps:
  0 — Origem: 2 chips (URL / Iniciais)
  1 — Configurar: conteúdo dinâmico por origem
       - URL: campo URL + preview circular ao vivo
       - Iniciais: campo iniciais (max 2 chars) + 6 swatches de cor
  2 — Confirmar: preview circular grande do avatar final
  3 — Sucesso

State: source, url, initials, bg_color.
`on_complete` recebe `{"source": str, "value": str}`, onde `source` é
`"Iniciais"` ou `"URL"` e `value` é `initials` / `url` correspondente.

`mock=True` inicializa com `PROFILE_AVATAR` (source="Iniciais", "AL",
roxo `#7C6EF6`) e abre no step 2 (Confirmar).
"""

import inspect
from dataclasses import dataclass
from typing import Awaitable, Callable, ClassVar

import flet as ft
from loguru import logger

from flet_wizards.core import (
    BaseWizardState,
    WizardFrame,
    WizardMeta,
    WizardTheme,
    form_field,
    primary_button,
    register,
)
from flet_wizards.core.mock_data import PROFILE_AVATAR

META = register(
    WizardMeta(
        id="profile.avatar",
        name="Avatar",
        category="profile",
        description="Wizard de configuração de avatar com 2 origens (iniciais ou URL).",
        steps=["Origem", "Configurar", "Confirmar"],
        platforms=[
            ft.PagePlatform.WINDOWS,
            ft.PagePlatform.MACOS,
            ft.PagePlatform.LINUX,
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
        ],
        on_complete_schema={"source": "'Iniciais'|'URL'", "value": "str"},
    )
)

SOURCE_OPTIONS: list[tuple[str, str]] = [
    ("URL", "🔗"),
    ("Iniciais", "✏️"),
]

AVATAR_COLORS: list[str] = [
    "#7C6EF6",
    "#34D399",
    "#F472B6",
    "#60A5FA",
    "#FB923C",
    "#A78BFA",
]


@ft.observable
@dataclass
class ProfileAvatarState(BaseWizardState):
    """Store reativo do ProfileAvatarWizard."""

    TOTAL_STEPS: ClassVar[int] = 3

    source: str = ""
    url: str = ""
    initials: str = ""
    bg_color: str = ""

    def reset(self) -> None:
        super().reset()
        self.source = ""
        self.url = ""
        self.initials = ""
        self.bg_color = ""


def _value_from_state(state: ProfileAvatarState) -> str:
    """Retorna o `value` apropriado conforme a origem selecionada."""
    if state.source == "Iniciais":
        return state.initials
    if state.source == "URL":
        return state.url
    return ""


def _avatar_circle(state: ProfileAvatarState, size: int) -> ft.Control:
    """Render circular do avatar conforme a origem corrente."""
    P = state.primary()
    B = state.border()
    radius = size // 2

    if state.source == "Iniciais":
        return ft.Container(
            width=size,
            height=size,
            border_radius=radius,
            bgcolor=state.bg_color or P,
            alignment=ft.Alignment(0, 0),
            content=ft.Text(
                (state.initials or "?").upper(),
                size=int(size * 0.38),
                color="#FFFFFF",
                weight=ft.FontWeight.BOLD,
            ),
        )
    if state.source == "URL" and state.url:
        return ft.Container(
            width=size,
            height=size,
            border_radius=radius,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Image(
                src=state.url,
                fit=ft.BoxFit.COVER,
                width=size,
                height=size,
            ),
        )
    return ft.Container(
        width=size,
        height=size,
        border_radius=radius,
        bgcolor=state.card(),
        border=ft.Border.all(1, B),
        alignment=ft.Alignment(0, 0),
        content=ft.Text("?", size=int(size * 0.4), color=state.sub()),
    )


@ft.component
def StepOrigem(state: ProfileAvatarState) -> ft.Control:
    """Seleção da fonte do avatar via 3 chips."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    source_v, set_source = ft.use_state(state.source)

    def pick(label: str):
        set_source(label)
        state.source = label

    def chip(label: str, icon: str) -> ft.GestureDetector:
        sel = source_v == label
        return ft.GestureDetector(
            on_tap=lambda _e, l=label: pick(l),
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Text(icon, size=14),
                        ft.Container(width=6),
                        ft.Text(
                            label,
                            size=12,
                            color="#FFFFFF" if sel else S,
                            weight=ft.FontWeight.W_600
                            if sel
                            else ft.FontWeight.W_400,
                        ),
                    ],
                    spacing=0,
                    tight=True,
                ),
                bgcolor=P if sel else C,
                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                border_radius=20,
                border=ft.Border.all(1, P if sel else B),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
            ),
        )

    return ft.Column(
        [
            ft.Text(
                "Origem do avatar",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Escolha como deseja configurar sua imagem de perfil.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            ft.Row(
                [chip(label, icon) for label, icon in SOURCE_OPTIONS],
                spacing=10,
            ),
        ],
        spacing=0,
    )


@ft.component
def _PanelIniciais(state: ProfileAvatarState) -> ft.Control:
    """Configurador para origem 'Iniciais' — texto + 6 swatches de cor."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    initials_v, set_initials = ft.use_state(state.initials)

    def on_initials(e):
        val = (e.control.value or "")[:2].upper()
        set_initials(val)
        state.initials = val

    def pick_color(c: str):
        state.bg_color = c

    def swatch(c: str) -> ft.GestureDetector:
        sel = state.bg_color == c
        return ft.GestureDetector(
            on_tap=lambda _e, color=c: pick_color(color),
            content=ft.Container(
                width=32,
                height=32,
                border_radius=16,
                bgcolor=c,
                border=ft.Border.all(2, "#FFFFFF" if sel else "transparent"),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
            ),
        )

    shared = dict(primary=P, text=T, sub=S, card=C, border=B)

    return ft.Column(
        [
            form_field("INICIAIS", initials_v, on_initials, "AB", **shared),
            ft.Container(height=22),
            ft.Text(
                "COR DO FUNDO",
                size=11,
                color=S,
                weight=ft.FontWeight.W_500,
                style=ft.TextStyle(letter_spacing=0.8),
            ),
            ft.Container(height=10),
            ft.Row([swatch(c) for c in AVATAR_COLORS], spacing=10),
        ],
        spacing=0,
    )


@ft.component
def _PanelURL(state: ProfileAvatarState) -> ft.Control:
    """Configurador para origem 'URL' — campo + preview circular."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    url_v, set_url = ft.use_state(state.url)

    def on_url(e):
        set_url(e.control.value)
        state.url = e.control.value

    shared = dict(primary=P, text=T, sub=S, card=C, border=B)

    return ft.Column(
        [
            form_field(
                "URL DA IMAGEM",
                url_v,
                on_url,
                "https://...",
                **shared,
            ),
            ft.Container(height=18),
            ft.Text(
                "PREVIEW",
                size=11,
                color=S,
                weight=ft.FontWeight.W_500,
                style=ft.TextStyle(letter_spacing=0.8),
            ),
            ft.Container(height=10),
            _avatar_circle(state, 96),
        ],
        spacing=0,
    )


@ft.component
def StepConfigurar(state: ProfileAvatarState) -> ft.Control:
    """Conteúdo dinâmico baseado em `state.source`."""

    T = state.text()
    S = state.sub()

    if state.source == "Iniciais":
        panel = _PanelIniciais(state)
    elif state.source == "URL":
        panel = _PanelURL(state)
    else:
        panel = ft.Text(
            "Volte ao step anterior e selecione uma origem.",
            size=13,
            color=S,
        )

    return ft.Column(
        [
            ft.Text(
                f"Configurar — {state.source or 'origem'}",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Ajuste os parâmetros desta origem.",
                size=13,
                color=S,
            ),
            ft.Container(height=24),
            panel,
        ],
        spacing=0,
    )


@ft.component
def StepConfirmarAvatar(state: ProfileAvatarState) -> ft.Control:
    """Preview final do avatar configurado."""

    T = state.text()
    S = state.sub()

    return ft.Column(
        [
            ft.Text(
                "Tudo pronto",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Confira como ficou o avatar antes de salvar.",
                size=13,
                color=S,
            ),
            ft.Container(height=32),
            ft.Container(
                content=_avatar_circle(state, 128),
                alignment=ft.Alignment(0, 0),
            ),
            ft.Container(height=18),
            ft.Text(
                f"Origem: {state.source or '—'}",
                size=12,
                color=S,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@ft.component
def StepSuccess(state: ProfileAvatarState) -> ft.Control:
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
                        "Avatar salvo.",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=T,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Sua nova imagem de perfil está ativa.",
                        size=13,
                        color=S,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=28),
                    primary_button("Voltar ao início", lambda _: state.reset(), P),
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
def ProfileAvatarWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: CompleteCallback | None = None,
    mock: bool = False,
) -> ft.Control:
    """Wizard público de avatar — 3 steps + sucesso.

    `mock=True` inicializa com `PROFILE_AVATAR` (source='Iniciais', 'AL',
    roxo) e abre no step 2 (Confirmar) já mostrando o preview circular.
    """

    if mock:
        initial = ProfileAvatarState(
            theme=theme,
            step=ProfileAvatarState.TOTAL_STEPS - 1,
            **PROFILE_AVATAR,
        )
    else:
        initial = ProfileAvatarState(theme=theme)

    state, _ = ft.use_state(initial)
    if state.theme != theme:
        state.theme = theme

    async def _adapt(s: ProfileAvatarState) -> None:
        if on_complete is None:
            logger.warning(
                "[ProfileAvatarWizard]: on_complete não fornecido — wizard funcionará como demo"
            )
            return
        result = on_complete(
            {"source": s.source, "value": _value_from_state(s)}
        )
        if inspect.isawaitable(result):
            await result

    return WizardFrame(
        state=state,
        step_labels=["Origem", "Configurar", "Confirmar"],
        step_hints=["Tipo do avatar", "Detalhes", "Preview final"],
        steps=[StepOrigem, StepConfigurar, StepConfirmarAvatar, StepSuccess],
        on_complete=_adapt,
        last_step_label="Salvar avatar",
        loading_label="Salvando...",
    )
