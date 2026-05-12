"""AuthTwoFactorWizard — verificação em dois fatores mobile-first.

Vibe: seguro, focado, minimalista. Sem distração visual — só o essencial.
Mobile-first com fundo levemente texturizado por uma malha geométrica de
pontos posicionada com `ft.Stack`, transmitindo a sensação de "ambiente
seguro" sem recorrer a imagens (mantém o pacote leve).

Steps:
  0 — Código: instrução + 6 campos individuais de dígito (1 char cada),
      reutilizando o padrão consolidado em `auth/recovery.py`
  1 — Sucesso: escudo grande verde + mensagem de confirmação

State: `code` armazenado como str padded com espaços; helpers `_get_digit`
e `_set_digit` manipulam por posição (mesmo contrato de `recovery.py`).

`on_complete` recebe `{"code": str}` — a aplicação cliente é responsável
por validar o código contra o backend. `mock=True` abre direto no step
do código já preenchido para preview rápido no gallery.
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
from flet_wizards.core.mock_data import AUTH_TWO_FACTOR
from flet_wizards.core.snack import show_error, show_info

META = register(
    WizardMeta(
        id="auth.two_factor",
        name="Verificação em 2 Fatores",
        category="auth",
        description="Wizard de 2FA mobile com 6 dígitos individuais e fundo geométrico.",
        steps=["Código"],
        platforms=[ft.PagePlatform.ANDROID, ft.PagePlatform.IOS],
        on_complete_schema={"code": "str"},
    )
)

CODE_LEN = 6
PAD_CHAR = " "


@ft.observable
@dataclass
class AuthTwoFactorState(BaseWizardState):
    """Store reativo do AuthTwoFactorWizard."""

    TOTAL_STEPS: ClassVar[int] = 1

    code: str = ""

    def reset(self) -> None:
        super().reset()
        self.code = ""


def _get_digit(code: str, i: int) -> str:
    if i >= len(code):
        return ""
    c = code[i]
    return "" if c == PAD_CHAR else c


def _set_digit(current: str, i: int, raw: str) -> str:
    val = (raw or "")[:1] or PAD_CHAR
    chars = list(current.ljust(CODE_LEN, PAD_CHAR))[:CODE_LEN]
    chars[i] = val
    return "".join(chars).rstrip(PAD_CHAR)


def _filled_digits(code: str) -> int:
    """Conta quantos dígitos não-PAD existem no buffer."""
    return sum(1 for c in code if c != PAD_CHAR)


@ft.component
def _GeometricBackdrop(state: AuthTwoFactorState) -> ft.Control:
    """Malha sutil de pontos geométricos transmitindo ambiente seguro.

    Implementada como Stack com `ft.Container` posicionados em alignments
    fixos — barato de renderizar e não exige imagem externa.
    """
    P = state.primary()
    B = state.border()

    def dot(size: int, color: str, opacity: float, ax: float, ay: float) -> ft.Control:
        return ft.Container(
            alignment=ft.Alignment(ax, ay),
            content=ft.Container(
                width=size,
                height=size,
                border_radius=size / 2,
                bgcolor=color,
                opacity=opacity,
            ),
        )

    def ring(size: int, color: str, opacity: float, ax: float, ay: float) -> ft.Control:
        return ft.Container(
            alignment=ft.Alignment(ax, ay),
            content=ft.Container(
                width=size,
                height=size,
                border_radius=size / 2,
                border=ft.Border.all(1, color),
                opacity=opacity,
            ),
        )

    children: list[ft.Control] = [
        ring(180, P, 0.12, -0.9, -0.85),
        ring(120, P, 0.10, 0.95, -0.7),
        ring(220, P, 0.08, 1.0, 0.9),
        ring(150, P, 0.10, -1.0, 0.95),
        dot(6, P, 0.35, -0.6, -0.55),
        dot(4, P, 0.40, 0.4, -0.45),
        dot(5, P, 0.30, 0.7, 0.2),
        dot(4, P, 0.35, -0.7, 0.4),
        dot(6, B, 0.55, 0.0, -0.78),
        dot(6, B, 0.55, 0.0, 0.78),
        dot(3, P, 0.45, 0.85, 0.55),
        dot(3, P, 0.45, -0.85, -0.2),
    ]

    return ft.Stack(children, expand=True)


@ft.component
def StepCodigo(state: AuthTwoFactorState) -> ft.Control:
    """Instrução + 6 campos individuais para o código de verificação."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    code_v, set_code = ft.use_state(state.code)

    def on_change(i: int):
        def handler(e):
            val = e.control.value or ""
            new_code = _set_digit(code_v, i, val)
            set_code(new_code)
            state.code = new_code

        return handler

    def digit_field(i: int) -> ft.Control:
        is_filled = bool(_get_digit(code_v, i))
        return ft.TextField(
            value=_get_digit(code_v, i),
            on_change=on_change(i),
            text_align=ft.TextAlign.CENTER,
            text_size=22,
            width=46,
            height=58,
            max_length=1,
            border_color=P if is_filled else B,
            focused_border_color=P,
            color=T,
            bgcolor=C,
            border_radius=10,
            content_padding=ft.Padding.symmetric(horizontal=0, vertical=8),
            cursor_color=P,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

    shield = ft.Container(
        width=64,
        height=64,
        border_radius=32,
        bgcolor=P,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("🛡️", size=28),
    )

    return ft.Column(
        [
            ft.Container(expand=1),
            shield,
            ft.Container(height=22),
            ft.Text(
                "Verificação de segurança",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=8),
            ft.Container(
                width=320,
                content=ft.Text(
                    "Digite o código de 6 dígitos gerado pelo seu app autenticador.",
                    size=13,
                    color=S,
                    text_align=ft.TextAlign.CENTER,
                ),
            ),
            ft.Container(height=32),
            ft.Row(
                [digit_field(i) for i in range(CODE_LEN)],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Container(height=18),
            ft.Text(
                "O código expira em 30 segundos.",
                size=11,
                color=S,
                text_align=ft.TextAlign.CENTER,
                weight=ft.FontWeight.W_500,
            ),
            ft.Container(expand=1),
        ],
        spacing=0,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


@ft.component
def StepSuccess(state: AuthTwoFactorState) -> ft.Control:
    """Confirmação visual — escudo grande sem fundo + mensagem de acesso liberado."""

    T = state.text()
    S = state.sub()
    P = state.primary()

    shield = ft.Text("🛡", size=80, text_align=ft.TextAlign.CENTER)

    return ft.Column(
        [
            ft.Container(expand=1),
            shield,
            ft.Container(height=24),
            ft.Text(
                "Identidade confirmada",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=10),
            ft.Container(
                width=300,
                content=ft.Text(
                    "Tudo seguro. Você já pode continuar para o app.",
                    size=13,
                    color=S,
                    text_align=ft.TextAlign.CENTER,
                ),
            ),
            ft.Container(height=32),
            primary_button("Voltar ao início", lambda _: state.reset(), P),
            ft.Container(expand=1),
        ],
        spacing=0,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


CompleteCallback = Callable[[dict], "None | Awaitable[None]"]


@ft.component
def AuthTwoFactorWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: CompleteCallback | None = None,
    mock: bool = False,
) -> ft.Control:
    """Wizard público de 2FA — 1 step + sucesso, reativo a `theme`.

    Validação local: exige os 6 dígitos preenchidos antes de avançar.
    `on_complete` é responsabilidade do consumidor — a lib não conhece o
    backend, apenas entrega o código digitado.

    `mock=True` inicializa com `AUTH_TWO_FACTOR` e abre no step 0 já
    com os dígitos preenchidos para servir de preview no gallery.
    """

    initial = (
        AuthTwoFactorState(
            theme=theme,
            step=0,
            **AUTH_TWO_FACTOR,
        )
        if mock
        else AuthTwoFactorState(theme=theme)
    )
    state, _ = ft.use_state(initial)
    if state.theme != theme:
        state.theme = theme

    P = state.primary()
    T = state.text()
    B = state.border()

    is_done = state.is_done()

    async def handle_confirm(_):
        if is_done:
            return
        if _filled_digits(state.code) < CODE_LEN:
            show_error("Preencha os 6 dígitos para confirmar.")
            return
        if state.loading:
            return
        state.loading = True
        try:
            if on_complete is not None:
                result = on_complete({"code": state.code})
                if inspect.isawaitable(result):
                    await result
            else:
                logger.warning(
                    "[AuthTwoFactorWizard]: on_complete não fornecido — wizard funcionará como demo"
                )
        except Exception as exc:
            logger.exception("on_complete falhou: {}", exc)
            show_error("Não foi possível verificar agora. Tente novamente.")
            state.loading = False
            return
        state.loading = False
        state.step = AuthTwoFactorState.TOTAL_STEPS

    body: ft.Control = StepSuccess(state) if is_done else StepCodigo(state)

    cta = (
        primary_button(
            "Confirmar",
            handle_confirm,
            P,
            loading=state.loading,
            loading_label="Verificando...",
        )
        if not is_done
        else ft.Container(width=0, height=0)
    )

    helper_row = (
        ft.Row(
            [
                ft.Container(expand=1),
                ft.GestureDetector(
                    on_tap=lambda _e: show_info(
                        "Reenvio de código é responsabilidade do app consumidor."
                    ),
                    content=ft.Container(
                        content=ft.Text(
                            "Reenviar código",
                            size=12,
                            color=T,
                            weight=ft.FontWeight.W_500,
                        ),
                        padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                        border_radius=8,
                        border=ft.Border.all(1, B),
                    ),
                ),
                ft.Container(expand=1),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        if not is_done
        else ft.Container(height=0)
    )

    content_area = ft.AnimatedSwitcher(
        content=ft.Container(
            key=str(state.step),
            content=body,
            expand=True,
        ),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=280,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_CUBIC,
        switch_out_curve=ft.AnimationCurve.EASE_IN_CUBIC,
        expand=True,
    )

    nav = (
        ft.Column(
            [
                ft.Row(
                    [ft.Container(expand=1), cta, ft.Container(expand=1)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(height=14),
                helper_row,
            ],
            spacing=0,
        )
        if not is_done
        else ft.Container(height=0)
    )

    foreground = ft.Container(
        expand=True,
        padding=ft.Padding.only(left=24, right=24, top=28, bottom=28),
        content=ft.Column(
            [
                ft.Container(content=content_area, expand=1),
                nav,
            ],
            spacing=0,
            expand=True,
        ),
    )

    return ft.Container(
        expand=True,
        bgcolor=state.bg(),
        animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT_CUBIC),
        content=ft.Stack(
            [
                _GeometricBackdrop(state),
                foreground,
            ],
            expand=True,
        ),
    )
