"""SurveyFeedbackWizard — questionário leve e conversacional em 3 perguntas.

Vibe estilo Typeform: uma pergunta por tela, fonte grande, inputs com
personalidade. Mobile-first, sem sidebar. O usuário sente que está
respondendo a um amigo, não preenchendo um formulário.

Steps:
  0 — NPS (0-10) em row de chips numerados, coloridos por faixa
      (0-6 vermelho, 7-8 amarelo, 9-10 verde)
  1 — Texto livre "o que motivou sua nota?" com contador de caracteres
  2 — Categoria do feedback em 3 cards grandes (Bug, Sugestão, Elogio)
  3 — Sucesso com agradecimento

Contexto fictício do mock: app "DevFlow", produto interno de revisão
de PRs. Os textos contextualizam a entrega como o time pedindo retorno
após uma atualização.

`on_complete` recebe `{"nps": int, "comment": str, "category": str}`.
`mock=True` abre direto no step 2 (categoria) com dados pré-populados.
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
from flet_wizards.core.mock_data import SURVEY_FEEDBACK
from flet_wizards.core.snack import show_error

META = register(
    WizardMeta(
        id="survey.feedback",
        name="Pesquisa de Feedback",
        category="survey",
        description="Survey conversacional estilo Typeform com NPS, comentário e categoria.",
        steps=["Nota", "Motivo", "Categoria"],
        platforms=[ft.PagePlatform.ANDROID, ft.PagePlatform.IOS],
        on_complete_schema={
            "nps": "int",
            "comment": "str",
            "category": "str",
        },
    )
)

COMMENT_LIMIT = 280

NPS_COLOR_DETRACTOR = "#EF4444"
NPS_COLOR_PASSIVE = "#F59E0B"
NPS_COLOR_PROMOTER = "#22C55E"


def _nps_color(value: int) -> str:
    """Devolve a cor da faixa NPS — detrator, passivo ou promotor."""
    if value <= 6:
        return NPS_COLOR_DETRACTOR
    if value <= 8:
        return NPS_COLOR_PASSIVE
    return NPS_COLOR_PROMOTER


CATEGORIES: list[tuple[str, str, str]] = [
    ("Bug", "🐞", "Algo não está funcionando como esperado."),
    ("Sugestão", "💡", "Uma ideia que melhoraria a experiência."),
    ("Elogio", "💚", "Algo que está agradando bastante."),
]


@ft.observable
@dataclass
class SurveyFeedbackState(BaseWizardState):
    """Store reativo do SurveyFeedbackWizard."""

    TOTAL_STEPS: ClassVar[int] = 3

    nps: int = -1
    comment: str = ""
    category: str = ""

    def reset(self) -> None:
        super().reset()
        self.nps = -1
        self.comment = ""
        self.category = ""


@ft.component
def _ProgressLine(state: SurveyFeedbackState) -> ft.Control:
    """Cabeçalho fino com contagem e barra de progresso."""
    P = state.primary()
    S = state.sub()
    B = state.border()

    total = SurveyFeedbackState.TOTAL_STEPS
    idx = min(state.step, total - 1)
    pct = (idx + 1) / total

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text(
                        "DevFlow · feedback",
                        size=11,
                        color=S,
                        weight=ft.FontWeight.W_500,
                        style=ft.TextStyle(letter_spacing=0.6),
                    ),
                    ft.Container(expand=1),
                    ft.Text(
                        f"{idx + 1} de {total}",
                        size=11,
                        color=S,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
            ft.Container(height=10),
            ft.Container(
                height=3,
                bgcolor=B,
                border_radius=2,
                content=ft.Container(
                    width=max(6.0, 320 * pct),
                    height=3,
                    bgcolor=P,
                    border_radius=2,
                    animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
                ),
                alignment=ft.Alignment(-1, 0),
            ),
        ],
        spacing=0,
    )


@ft.component
def StepNPS(state: SurveyFeedbackState) -> ft.Control:
    """Row de chips 0-10 — selecionar pinta com a cor da faixa."""

    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    selected, set_selected = ft.use_state(state.nps)

    def pick(value: int):
        def handler(_e):
            set_selected(value)
            state.nps = value

        return handler

    def chip(value: int) -> ft.Control:
        is_selected = selected == value
        color = _nps_color(value)
        return ft.GestureDetector(
            on_tap=pick(value),
            content=ft.Container(
                width=36,
                height=44,
                border_radius=10,
                bgcolor=color if is_selected else C,
                border=ft.Border.all(1, color if is_selected else B),
                alignment=ft.Alignment(0, 0),
                content=ft.Text(
                    str(value),
                    size=15,
                    color="#FFFFFF" if is_selected else T,
                    weight=ft.FontWeight.BOLD,
                ),
                animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT_CUBIC),
            ),
        )

    legend = ft.Row(
        [
            ft.Text("Pouco provável", size=10, color=S),
            ft.Container(expand=1),
            ft.Text("Muito provável", size=10, color=S),
        ],
    )

    return ft.Column(
        [
            ft.Text(
                "Em uma escala de 0 a 10,",
                size=15,
                color=S,
                weight=ft.FontWeight.W_500,
            ),
            ft.Container(height=4),
            ft.Text(
                "qual a chance de você recomendar o DevFlow para outra dev?",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=36),
            ft.Row(
                [chip(i) for i in range(11)],
                spacing=6,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(height=10),
            legend,
        ],
        spacing=0,
    )


@ft.component
def StepComentario(state: SurveyFeedbackState) -> ft.Control:
    """Texto livre com contador de caracteres."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    comment_v, set_comment = ft.use_state(state.comment)

    def on_change(e):
        val = (e.control.value or "")[:COMMENT_LIMIT]
        set_comment(val)
        state.comment = val

    used = len(comment_v)
    near_limit = used >= int(COMMENT_LIMIT * 0.9)

    return ft.Column(
        [
            ft.Text(
                "Anotado.",
                size=15,
                color=S,
                weight=ft.FontWeight.W_500,
            ),
            ft.Container(height=4),
            ft.Text(
                "O que motivou essa nota?",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=8),
            ft.Text(
                "Pode ser uma frase ou um parágrafo — o que vier à cabeça.",
                size=13,
                color=S,
            ),
            ft.Container(height=22),
            ft.TextField(
                value=comment_v,
                on_change=on_change,
                multiline=True,
                min_lines=4,
                max_lines=6,
                border_color=B,
                focused_border_color=P,
                color=T,
                bgcolor=C,
                border_radius=10,
                hint_text="Conte aqui...",
                hint_style=ft.TextStyle(color=S, size=14),
                text_size=14,
                cursor_color=P,
                content_padding=ft.Padding.all(14),
            ),
            ft.Container(height=8),
            ft.Row(
                [
                    ft.Container(expand=1),
                    ft.Text(
                        f"{used}/{COMMENT_LIMIT}",
                        size=11,
                        color=NPS_COLOR_PASSIVE if near_limit else S,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
            ),
        ],
        spacing=0,
    )


@ft.component
def StepCategoria(state: SurveyFeedbackState) -> ft.Control:
    """3 cards grandes para classificar o feedback."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    selected, set_selected = ft.use_state(state.category)

    def pick(label: str):
        def handler(_e):
            set_selected(label)
            state.category = label

        return handler

    def card(label: str, glyph: str, description: str) -> ft.Control:
        is_selected = selected == label
        return ft.GestureDetector(
            on_tap=pick(label),
            content=ft.Container(
                padding=ft.Padding.all(16),
                bgcolor=C,
                border_radius=12,
                border=ft.Border.all(2 if is_selected else 1, P if is_selected else B),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
                content=ft.Row(
                    [
                        ft.Container(
                            width=44,
                            height=44,
                            border_radius=22,
                            bgcolor=P if is_selected else state.panel(),
                            alignment=ft.Alignment(0, 0),
                            content=ft.Text(glyph, size=22),
                            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
                        ),
                        ft.Container(width=14),
                        ft.Column(
                            [
                                ft.Text(
                                    label,
                                    size=15,
                                    color=T,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(height=2),
                                ft.Text(description, size=12, color=S),
                            ],
                            spacing=0,
                            expand=1,
                        ),
                        ft.Container(
                            width=22,
                            height=22,
                            border_radius=11,
                            bgcolor=P if is_selected else "transparent",
                            border=ft.Border.all(1, P if is_selected else B),
                            alignment=ft.Alignment(0, 0),
                            content=ft.Text(
                                "✓" if is_selected else "",
                                size=12,
                                color="#FFFFFF",
                                weight=ft.FontWeight.BOLD,
                            ),
                            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT_CUBIC),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        )

    return ft.Column(
        [
            ft.Text(
                "Última pergunta.",
                size=15,
                color=S,
                weight=ft.FontWeight.W_500,
            ),
            ft.Container(height=4),
            ft.Text(
                "Como você classificaria esse retorno?",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=22),
            *[
                ft.Container(
                    content=card(label, glyph, desc),
                    margin=ft.Margin(0, 0, 0, 10),
                )
                for label, glyph, desc in CATEGORIES
            ],
        ],
        spacing=0,
    )


@ft.component
def StepSuccess(state: SurveyFeedbackState) -> ft.Control:
    """Agradecimento final com resumo curto e reset."""

    P = state.primary()
    T = state.text()
    S = state.sub()

    check = ft.Container(
        width=80,
        height=80,
        border_radius=40,
        bgcolor=P,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("✓", size=40, color="#FFFFFF", weight=ft.FontWeight.BOLD),
    )

    summary = (
        f"Nota {state.nps} · {state.category or 'sem categoria'}"
        if state.nps >= 0
        else "Feedback registrado."
    )

    return ft.Column(
        [
            ft.Container(expand=1),
            check,
            ft.Container(height=22),
            ft.Text(
                "Obrigado pelo retorno!",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=8),
            ft.Container(
                width=300,
                content=ft.Text(
                    "O time do DevFlow lê todas as respostas e prioriza pelo impacto.",
                    size=13,
                    color=S,
                    text_align=ft.TextAlign.CENTER,
                ),
            ),
            ft.Container(height=14),
            ft.Text(summary, size=12, color=S, weight=ft.FontWeight.W_500),
            ft.Container(height=28),
            primary_button(
                "Enviar outro",
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
def SurveyFeedbackWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: CompleteCallback | None = None,
    mock: bool = False,
) -> ft.Control:
    """Wizard público de feedback — 3 steps + sucesso, reativo a `theme`.

    Validação por step: NPS exige seleção (>=0), comentário aceita vazio,
    categoria exige seleção. Se a validação falhar, dispara snack de erro
    em vez de avançar.

    `mock=True` abre direto no step 2 (categoria) com `SURVEY_FEEDBACK`.
    """

    initial = (
        SurveyFeedbackState(
            theme=theme,
            step=SurveyFeedbackState.TOTAL_STEPS - 1,
            **SURVEY_FEEDBACK,
        )
        if mock
        else SurveyFeedbackState(theme=theme)
    )
    state, _ = ft.use_state(initial)
    if state.theme != theme:
        state.theme = theme

    total = SurveyFeedbackState.TOTAL_STEPS
    is_last = state.step == total - 1
    is_done = state.is_done()

    P = state.primary()
    T = state.text()
    B = state.border()

    def validate_current() -> bool:
        if state.step == 0 and state.nps < 0:
            show_error("Selecione uma nota de 0 a 10 antes de continuar.")
            return False
        if state.step == 2 and not state.category:
            show_error("Escolha uma categoria para enviar o feedback.")
            return False
        return True

    async def handle_advance(_):
        if is_done:
            return
        if not validate_current():
            return
        if is_last:
            if state.loading:
                return
            state.loading = True
            try:
                if on_complete is not None:
                    payload = {
                        "nps": state.nps,
                        "comment": state.comment,
                        "category": state.category,
                    }
                    result = on_complete(payload)
                    if inspect.isawaitable(result):
                        await result
                else:
                    logger.warning(
                        "[SurveyFeedbackWizard]: on_complete não fornecido — wizard funcionará como demo"
                    )
            except Exception as exc:
                logger.exception("on_complete falhou: {}", exc)
                show_error("Não foi possível enviar agora. Tente novamente.")
                state.loading = False
                return
            state.loading = False
            state.step = total
        else:
            state.go_next()

    if is_done:
        body: ft.Control = StepSuccess(state)
    elif state.step == 0:
        body = StepNPS(state)
    elif state.step == 1:
        body = StepComentario(state)
    else:
        body = StepCategoria(state)

    cta_label = "Enviar" if is_last else "Continuar"
    cta = primary_button(
        cta_label,
        handle_advance,
        P,
        loading=state.loading and is_last,
        loading_label="Enviando...",
        mode=state.theme.mode,
    )

    back = (
        ft.GestureDetector(
            on_tap=lambda _e: state.go_back(),
            content=ft.Container(
                content=ft.Text(
                    "← Voltar",
                    size=13,
                    color=T,
                    weight=ft.FontWeight.W_500,
                ),
                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            ),
        )
        if state.step > 0 and not is_done
        else ft.Container(width=0, height=40)
    )

    header = _ProgressLine(state) if not is_done else ft.Container(height=0)

    content_area = ft.AnimatedSwitcher(
        content=ft.Container(
            key=str(state.step),
            content=body,
            expand=True,
        ),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=260,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_CUBIC,
        switch_out_curve=ft.AnimationCurve.EASE_IN_CUBIC,
        expand=True,
    )

    nav = (
        ft.Row(
            [back, ft.Container(expand=1), cta],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        if not is_done
        else ft.Container(height=0)
    )

    return ft.Container(
        expand=True,
        bgcolor=state.bg(),
        padding=ft.Padding.only(left=22, right=22, top=20, bottom=24),
        animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
        content=ft.Column(
            [
                header,
                ft.Container(height=26 if not is_done else 0),
                ft.Container(content=content_area, expand=1),
                ft.Container(
                    height=1,
                    bgcolor=B,
                    margin=ft.Margin(0, 14, 0, 14),
                    visible=not is_done,
                ),
                nav,
            ],
            spacing=0,
            expand=True,
        ),
    )
