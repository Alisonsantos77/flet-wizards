"""OnboardingWalkthroughWizard — walkthrough mobile fullscreen em 4 slides.

Vibe: acolhedor, animado, fullscreen. Sem sidebar — wizard mobile-first
desenhado para Android/iOS, com slides ocupando a tela inteira:

  - cabeçalho com "Pular" alinhado à direita (some no último slide)
  - ícone grande centralizado em círculo colorido
  - título e subtítulo abaixo do ícone
  - dots de progresso no bottom
  - botão pill flutuante: "Próximo →" nos slides 0-2, "Começar" no slide 3

`state.step` controla o slide ativo (0..3). `is_done()` (step == 4) renderiza
a tela curta de sucesso com check + reset. `on_complete` é disparado no
clique de "Começar" e recebe `{}` — não há dados a coletar, apenas a
sinalização de que o usuário concluiu o onboarding.

`mock=True` abre direto no slide 3 (CTA "Começar") como preview rápido.
"""

import inspect
from dataclasses import dataclass
from typing import Awaitable, Callable, ClassVar

import flet as ft
from loguru import logger

from flet_wizards.core import (
    BaseWizardState,
    WizardMeta,
    WizardTheme,
    primary_button,
    register,
)
from flet_wizards.core.snack import show_error

META = register(
    WizardMeta(
        id="onboarding.walkthrough",
        name="Walkthrough de Boas-vindas",
        category="onboarding",
        description="Walkthrough mobile fullscreen em 4 slides com CTA final.",
        steps=["Bem-vindo", "Organize", "Acompanhe", "Comece"],
        platforms=[ft.PagePlatform.ANDROID, ft.PagePlatform.IOS],
        on_complete_schema={},
    )
)


@dataclass(frozen=True)
class _Slide:
    """Conteúdo declarativo de um slide do walkthrough."""

    glyph: str
    title: str
    subtitle: str


SLIDES: list[_Slide] = [
    _Slide(
        glyph="✨",
        title="Bem-vindo ao DayFlow",
        subtitle="Organize tarefas, hábitos e foco em um único lugar — sem fricção.",
    ),
    _Slide(
        glyph="📋",
        title="Organize seu dia",
        subtitle="Listas inteligentes que se adaptam ao seu ritmo e prioridades.",
    ),
    _Slide(
        glyph="📈",
        title="Acompanhe seu progresso",
        subtitle="Gráficos diários e streaks para manter o ímpeto sem cobrança.",
    ),
    _Slide(
        glyph="🚀",
        title="Pronto para começar?",
        subtitle="Tudo está configurado. Mergulhe e personalize conforme avança.",
    ),
]


@ft.observable
@dataclass
class OnboardingWalkthroughState(BaseWizardState):
    """Store reativo do OnboardingWalkthroughWizard."""

    TOTAL_STEPS: ClassVar[int] = len(SLIDES)

    def reset(self) -> None:
        super().reset()


@ft.component
def _Dot(active: bool, color_on: str, color_off: str) -> ft.Control:
    """Indicador de slide — pílula quando ativo, círculo pequeno quando inativo."""
    return ft.Container(
        width=22 if active else 8,
        height=8,
        border_radius=4,
        bgcolor=color_on if active else color_off,
        animate=ft.Animation(280, ft.AnimationCurve.EASE_OUT_CUBIC),
    )


@ft.component
def _IconBadge(state: OnboardingWalkthroughState, glyph: str) -> ft.Control:
    """Ícone grande centralizado em badge circular com halo suave."""
    P = state.primary()
    S2 = state.secondary()

    halo = ft.Container(
        width=200,
        height=200,
        border_radius=100,
        bgcolor=S2,
        opacity=0.12,
        animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
    )
    inner = ft.Container(
        width=140,
        height=140,
        border_radius=70,
        bgcolor=P,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(glyph, size=64, text_align=ft.TextAlign.CENTER),
        animate=ft.Animation(360, ft.AnimationCurve.EASE_OUT_CUBIC),
    )

    return ft.Stack(
        [
            ft.Container(content=halo, alignment=ft.Alignment(0, 0)),
            ft.Container(content=inner, alignment=ft.Alignment(0, 0)),
        ],
        width=200,
        height=200,
        alignment=ft.Alignment(0, 0),
    )


@ft.component
def _Slide_View(state: OnboardingWalkthroughState, slide: _Slide) -> ft.Control:
    """Bloco visual do slide ativo — ícone grande + título + subtítulo."""
    T = state.text()
    S = state.sub()

    return ft.Column(
        [
            _IconBadge(state, slide.glyph),
            ft.Container(height=36),
            ft.Text(
                slide.title,
                size=24,
                weight=ft.FontWeight.BOLD,
                color=T,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=12),
            ft.Container(
                width=320,
                content=ft.Text(
                    slide.subtitle,
                    size=14,
                    color=S,
                    text_align=ft.TextAlign.CENTER,
                ),
            ),
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@ft.component
def _SuccessView(state: OnboardingWalkthroughState) -> ft.Control:
    """Confirmação curta após o usuário concluir o walkthrough."""
    P = state.primary()
    T = state.text()
    S = state.sub()

    check = ft.Container(
        width=88,
        height=88,
        border_radius=44,
        bgcolor=P,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("✓", size=44, color="#FFFFFF", weight=ft.FontWeight.BOLD),
    )

    return ft.Column(
        [
            ft.Container(expand=1),
            check,
            ft.Container(height=22),
            ft.Text(
                "Tudo pronto!",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=8),
            ft.Container(
                width=300,
                content=ft.Text(
                    "Aproveite a experiência. Você pode rever o tour nas configurações.",
                    size=13,
                    color=S,
                    text_align=ft.TextAlign.CENTER,
                ),
            ),
            ft.Container(height=32),
            primary_button(
                "Refazer tour",
                lambda _: state.reset(),
                P,
                mode=state.theme.mode,
            ),
            ft.Container(expand=1),
        ],
        spacing=0,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


CompleteCallback = Callable[[dict], "None | Awaitable[None]"]


@ft.component
def OnboardingWalkthroughWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: CompleteCallback | None = None,
    mock: bool = False,
) -> ft.Control:
    """Walkthrough mobile fullscreen reativo a `theme`.

    `mock=True` abre direto no último slide (CTA "Começar"). O botão da
    barra inferior dispara `on_complete({})` no slide final e ativa o
    estado de loading enquanto a coroutine roda.
    """

    initial = (
        OnboardingWalkthroughState(
            theme=theme,
            step=OnboardingWalkthroughState.TOTAL_STEPS - 1,
        )
        if mock
        else OnboardingWalkthroughState(theme=theme)
    )
    state, _ = ft.use_state(initial)
    if state.theme != theme:
        state.theme = theme

    bg = state.bg()
    P = state.primary()
    S = state.sub()
    B = state.border()

    if state.is_done():
        body: ft.Control = _SuccessView(state)
    else:
        body = _Slide_View(state, SLIDES[state.step])

    total = OnboardingWalkthroughState.TOTAL_STEPS
    is_last = state.step == total - 1
    is_done = state.is_done()

    async def handle_advance(_):
        if is_done:
            return
        if is_last:
            if state.loading:
                return
            state.loading = True
            try:
                if on_complete is not None:
                    result = on_complete({})
                    if inspect.isawaitable(result):
                        await result
                else:
                    logger.warning(
                        "[OnboardingWalkthroughWizard]: on_complete não fornecido — wizard funcionará como demo"
                    )
            except Exception as exc:
                logger.exception("on_complete falhou: {}", exc)
                show_error("Não foi possível concluir o tour. Tente novamente.")
                state.loading = False
                return
            state.loading = False
            state.step = total
        else:
            state.go_next()

    cta_label = "Começar" if is_last else "Próximo →"
    cta = (
        ft.Container(
            content=primary_button(
                cta_label,
                handle_advance,
                P,
                loading=state.loading,
                loading_label="Preparando...",
                mode=state.theme.mode,
            ),
            padding=ft.Padding.symmetric(horizontal=8, vertical=0),
        )
        if not is_done
        else ft.Container(width=0, height=0)
    )

    dots = ft.Row(
        [
            _Dot(active=(i == state.step), color_on=P, color_off=B)
            for i in range(total)
        ],
        spacing=6,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    skip = (
        ft.GestureDetector(
            on_tap=lambda _e: setattr(state, "step", total - 1),
            content=ft.Container(
                content=ft.Text(
                    "Pular",
                    size=13,
                    color=S,
                    weight=ft.FontWeight.W_500,
                ),
                padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            ),
        )
        if not is_last and not is_done
        else ft.Container(width=0, height=36)
    )

    header = ft.Row(
        [ft.Container(expand=1), skip],
        alignment=ft.MainAxisAlignment.END,
    )

    content_area = ft.AnimatedSwitcher(
        content=ft.Container(
            key=str(state.step),
            content=body,
            expand=True,
            alignment=ft.Alignment(0, 0),
        ),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=280,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_CUBIC,
        switch_out_curve=ft.AnimationCurve.EASE_IN_CUBIC,
        expand=True,
    )

    bottom_bar = (
        ft.Column(
            [
                dots,
                ft.Container(height=18),
                ft.Row(
                    [ft.Container(expand=1), cta, ft.Container(expand=1)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        if not is_done
        else ft.Container(height=0)
    )

    return ft.Container(
        expand=True,
        bgcolor=bg,
        padding=ft.Padding.only(left=20, right=20, top=20, bottom=28),
        animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
        content=ft.Column(
            [
                header,
                ft.Container(
                    content=content_area,
                    expand=1,
                    alignment=ft.Alignment(0, 0),
                ),
                bottom_bar,
            ],
            spacing=0,
            expand=True,
        ),
    )
