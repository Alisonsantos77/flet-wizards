"""Orquestrador genérico de wizards multi-step.

Reúne os três blocos visuais comuns a todos os templates:

- `Sidebar` — coluna esquerda com indicadores de step, conector animado
  e barra de progresso. Recebe `state`, rótulos e dicas dos steps.
- `NavBar` — barra inferior com Voltar / Continuar. O handler de avanço
  é async para suportar `on_complete` síncrono ou awaitable, ativando
  `state.loading` enquanto a coroutine roda. Falhas no `on_complete`
  são logadas via loguru e expostas ao usuário via `snack.show_error`.
- `WizardFrame` — o orquestrador: Sidebar + content (`AnimatedSwitcher`
  com `key=str(state.step)`, indispensável para a transição funcionar) +
  NavBar, dentro do frame com border/bgcolor do tema.

Cada wizard concreto se reduz a:

```python
@ft.component
def MeuWizard(theme=WizardTheme.SLATE, on_complete=None) -> ft.Control:
    state, _ = ft.use_state(MeuState(theme=theme))
    return WizardFrame(
        state=state,
        step_labels=["A", "B"],
        step_hints=["...", "..."],
        steps=[StepA, StepB, StepSuccess],
        on_complete=on_complete,
    )
```
"""

import inspect
from typing import Awaitable, Callable

import flet as ft
from loguru import logger

from .base_state import BaseWizardState
from .components import divider, ghost_button, primary_button
from .snack import show_error

SIDE_W = 272

StepBuilder = Callable[[BaseWizardState], ft.Control]
CompleteHandler = Callable[[BaseWizardState], "None | Awaitable[None]"]


@ft.component
def Sidebar(
    state: BaseWizardState,
    step_labels: list[str],
    step_hints: list[str],
    title: str | None = None,
) -> ft.Control:
    """Coluna esquerda com indicadores de step e barra de progresso."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()

    is_done = state.is_done()
    total = state.TOTAL_STEPS

    def step_row(i: int, label: str, hint: str) -> ft.Column:
        done = state.step > i or is_done
        active = state.step == i and not is_done

        circle = ft.Container(
            content=ft.Text(
                "✓" if done else str(i + 1),
                size=10,
                color="#FFFFFF" if (done or active) else S,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            width=28,
            height=28,
            border_radius=14,
            bgcolor=P if (done or active) else "transparent",
            border=ft.Border.all(1, P if (done or active) else B),
            alignment=ft.Alignment(0, 0),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT_CUBIC),
        )

        indicator = ft.Container(
            width=3,
            height=32,
            bgcolor=P,
            border_radius=2,
            opacity=1.0 if active else 0.0,
            animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_OUT_CUBIC),
        )

        labels = ft.Column(
            [
                ft.Text(
                    label,
                    size=13,
                    color=T if active else (state.secondary() if done else S),
                    weight=ft.FontWeight.W_600 if active else ft.FontWeight.W_400,
                ),
                ft.Text(hint, size=11, color=S),
            ],
            spacing=1,
        )

        spacer = (
            ft.Container(height=14) if i < total - 1 else ft.Container(height=0)
        )

        return ft.Column(
            [
                ft.Row(
                    [
                        indicator,
                        ft.Container(width=10),
                        circle,
                        ft.Container(width=12),
                        labels,
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                spacer,
            ],
            spacing=0,
        )

    pct = 100 if is_done else int((state.step / max(total - 1, 1)) * 100)
    bar_w = SIDE_W - 48

    header: list[ft.Control] = []
    if title:
        header = [
            ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=T),
            ft.Container(height=24),
        ]

    progress_bar = ft.Container(
        height=3,
        bgcolor=B,
        border_radius=2,
        content=ft.Container(
            width=max(4, bar_w * pct / 100),
            height=3,
            bgcolor=P,
            border_radius=2,
            animate=ft.Animation(450, ft.AnimationCurve.EASE_OUT_CUBIC),
        ),
        alignment=ft.Alignment(-1, 0),
    )

    rows = [
        step_row(i, label, step_hints[i] if i < len(step_hints) else "")
        for i, label in enumerate(step_labels)
    ]

    return ft.Container(
        width=SIDE_W,
        bgcolor=state.panel(),
        padding=ft.Padding.symmetric(horizontal=24, vertical=28),
        border_radius=ft.BorderRadius.only(top_left=12, bottom_left=12),
        content=ft.Column(
            [
                *header,
                *rows,
                ft.Container(expand=1),
                divider(B),
                ft.Container(height=14),
                ft.Row(
                    [
                        ft.Text("Progresso", size=10, color=S),
                        ft.Container(expand=1),
                        ft.Text(
                            f"{pct}%",
                            size=10,
                            color=P,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),
                ft.Container(height=6),
                progress_bar,
                ft.Container(height=16),
            ],
            spacing=0,
            expand=True,
        ),
    )


@ft.component
def NavBar(
    state: BaseWizardState,
    on_complete: CompleteHandler | None,
    next_label: str = "Continuar →",
    last_step_label: str = "Concluir",
    loading_label: str = "Processando...",
) -> ft.Control:
    """Barra de navegação inferior. Some no step de conclusão."""

    if state.is_done():
        return ft.Container(height=0)

    P = state.primary()
    T = state.text()
    B = state.border()
    is_last = state.step == state.TOTAL_STEPS - 1

    back = (
        ghost_button("← Voltar", lambda _: state.go_back(), T, B)
        if state.step > 0
        else ft.Container()
    )

    async def handle_next(_):
        if is_last:
            if state.loading:
                return
            state.loading = True
            try:
                if on_complete is not None:
                    result = on_complete(state)
                    if inspect.isawaitable(result):
                        await result
            except Exception as exc:
                logger.exception("on_complete falhou: {}", exc)
                show_error("Não foi possível concluir. Tente novamente.")
                return
            finally:
                state.loading = False
            state.step = state.TOTAL_STEPS
        else:
            state.go_next()

    label = last_step_label if is_last else next_label
    nxt = primary_button(
        label,
        handle_next,
        P,
        loading=state.loading and is_last,
        loading_label=loading_label,
    )

    return ft.Row(
        [back, ft.Container(expand=1), nxt],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


@ft.component
def WizardFrame(
    state: BaseWizardState,
    step_labels: list[str],
    step_hints: list[str],
    steps: list[StepBuilder],
    on_complete: CompleteHandler | None = None,
    title: str | None = None,
    next_label: str = "Continuar →",
    last_step_label: str = "Concluir",
    loading_label: str = "Processando...",
) -> ft.Control:
    """Frame completo do wizard: Sidebar + content + NavBar.

    `steps` deve conter `state.TOTAL_STEPS + 1` builders: um por step de
    dados mais o de conclusão (success), nessa ordem. O AnimatedSwitcher
    usa `key=str(state.step)` — sem isso o Flet reaproveita o container
    e a transição fade não dispara.
    """

    B = state.border()
    C = state.card()

    current_index = min(state.step, len(steps) - 1)
    Current = steps[current_index]

    show_nav = not state.is_done()

    content_area = ft.AnimatedSwitcher(
        content=ft.Container(
            key=str(state.step),
            content=Current(state),
            expand=True,
        ),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=260,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_CUBIC,
        switch_out_curve=ft.AnimationCurve.EASE_IN_CUBIC,
        expand=True,
    )

    panel_children: list[ft.Control] = [
        ft.Container(
            content=content_area,
            expand=1,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        ),
    ]

    if show_nav:
        panel_children += [
            ft.Container(height=20),
            divider(B),
            ft.Container(height=16),
            NavBar(
                state=state,
                on_complete=on_complete,
                next_label=next_label,
                last_step_label=last_step_label,
                loading_label=loading_label,
            ),
        ]

    main_panel = ft.Container(
        expand=1,
        bgcolor=C,
        padding=ft.Padding.only(left=40, right=40, top=32, bottom=28),
        border_radius=ft.BorderRadius.only(top_right=12, bottom_right=12),
        content=ft.Column(panel_children, spacing=0, expand=True),
    )

    frame = ft.Container(
        expand=True,
        border_radius=12,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        border=ft.Border.all(1, B),
        animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
        content=ft.Row(
            [
                Sidebar(
                    state=state,
                    step_labels=step_labels,
                    step_hints=step_hints,
                    title=title,
                ),
                ft.Container(width=1, bgcolor=B),
                main_panel,
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True,
        ),
    )

    return ft.Container(
        expand=True,
        bgcolor=state.bg(),
        padding=ft.Padding.symmetric(horizontal=40, vertical=32),
        animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
        content=frame,
    )
