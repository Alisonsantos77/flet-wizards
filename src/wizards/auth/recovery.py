"""AuthRecoveryWizard — recuperação de senha em 3 steps.

Steps:
  0 — E-mail: campo de e-mail + instrução de envio do código
  1 — Código: 6 campos individuais lado a lado (1 char cada)
  2 — Nova senha: nova + confirmação + indicador de força
  3 — Sucesso

State: email, code, new_password, confirm_password.
`code` é armazenado como `str` padded com espaços; helpers `_get_digit` e
`_set_digit` manejam por posição. `on_complete` recebe `{"email": str}`.

`mock=True` inicializa com `AUTH_RECOVERY` e abre no step 2 (Nova senha).
"""

import inspect
from dataclasses import dataclass
from typing import Awaitable, Callable, ClassVar

import flet as ft

from wizards.core import (
    BaseWizardState,
    WizardFrame,
    WizardMeta,
    WizardTheme,
    form_field,
    primary_button,
    register,
)
from wizards.core.mock_data import AUTH_RECOVERY

META = register(
    WizardMeta(
        id="auth.recovery",
        name="Recuperar Senha",
        category="auth",
        description="Wizard de recuperação de senha com código de verificação.",
        steps=["E-mail", "Código", "Nova senha"],
        platforms=[
            ft.PagePlatform.WINDOWS,
            ft.PagePlatform.MACOS,
            ft.PagePlatform.LINUX,
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
        ],
        on_complete_schema={"email": "str"},
    )
)

CODE_LEN = 6
PAD_CHAR = " "


@ft.observable
@dataclass
class AuthRecoveryState(BaseWizardState):
    """Store reativo do AuthRecoveryWizard."""

    TOTAL_STEPS: ClassVar[int] = 3

    email: str = ""
    code: str = ""
    new_password: str = ""
    confirm_password: str = ""

    def reset(self) -> None:
        super().reset()
        self.email = ""
        self.code = ""
        self.new_password = ""
        self.confirm_password = ""


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


def _strength(password: str) -> tuple[str, str, float]:
    """Devolve (label, cor_hex, percentual 0..1) baseado em complexidade."""
    if not password:
        return ("", "#00000000", 0.0)
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isdigit() for c in password) and any(c.isalpha() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_+=[]{}|;:,.<>?/" for c in password):
        score += 1
    levels = [
        ("Muito fraca", "#EF4444", 0.2),
        ("Fraca", "#F59E0B", 0.4),
        ("Razoável", "#FACC15", 0.6),
        ("Boa", "#84CC16", 0.8),
        ("Forte", "#22C55E", 1.0),
    ]
    return levels[min(score, 4)]


@ft.component
def StepEmailRecovery(state: AuthRecoveryState) -> ft.Control:
    """Captura o e-mail da conta e instrui sobre o envio do código."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    email_v, set_email = ft.use_state(state.email)

    def on_email(e):
        set_email(e.control.value)
        state.email = e.control.value

    shared = dict(primary=P, text=T, sub=S, card=C, border=B)

    return ft.Column(
        [
            ft.Text(
                "Recuperar acesso",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Informe o e-mail da conta. Enviaremos um código de verificação.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            form_field("E-MAIL", email_v, on_email, "voce@exemplo.com", **shared),
        ],
        spacing=0,
    )


@ft.component
def StepCodigo(state: AuthRecoveryState) -> ft.Control:
    """6 campos individuais para o código de verificação."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    code_v, set_code = ft.use_state(state.code)

    def on_change(i: int):
        def handler(e):
            new_code = _set_digit(code_v, i, e.control.value)
            set_code(new_code)
            state.code = new_code

        return handler

    def digit_field(i: int) -> ft.TextField:
        return ft.TextField(
            value=_get_digit(code_v, i),
            on_change=on_change(i),
            text_align=ft.TextAlign.CENTER,
            text_size=20,
            width=48,
            height=56,
            max_length=1,
            border_color=B,
            focused_border_color=P,
            color=T,
            bgcolor=C,
            border_radius=8,
            content_padding=ft.Padding.symmetric(horizontal=0, vertical=8),
            cursor_color=P,
        )

    return ft.Column(
        [
            ft.Text(
                "Verifique o código",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                f"Enviamos um código de 6 dígitos para {state.email or 'seu e-mail'}.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            ft.Row(
                [digit_field(i) for i in range(CODE_LEN)],
                spacing=8,
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        spacing=0,
    )


@ft.component
def StepNovaSenha(state: AuthRecoveryState) -> ft.Control:
    """Nova senha + confirmação + indicador de força animado."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    new_v, set_new = ft.use_state(state.new_password)
    confirm_v, set_confirm = ft.use_state(state.confirm_password)

    def on_new(e):
        set_new(e.control.value)
        state.new_password = e.control.value

    def on_confirm(e):
        set_confirm(e.control.value)
        state.confirm_password = e.control.value

    shared = dict(primary=P, text=T, sub=S, card=C, border=B)
    label, color, pct = _strength(new_v)
    bar_w = 360
    mismatch = bool(confirm_v) and bool(new_v) and confirm_v != new_v

    return ft.Column(
        [
            ft.Text(
                "Defina a nova senha",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Use ao menos 8 caracteres com letras, números e símbolo.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            form_field(
                "NOVA SENHA",
                new_v,
                on_new,
                "Mínimo 8 caracteres",
                password=True,
                can_reveal_password=True,
                **shared,
            ),
            ft.Container(height=10),
            ft.Container(
                height=4,
                width=bar_w,
                bgcolor=B,
                border_radius=2,
                content=ft.Container(
                    width=max(0, bar_w * pct),
                    height=4,
                    bgcolor=color,
                    border_radius=2,
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT_CUBIC),
                ),
                alignment=ft.Alignment(-1, 0),
            ),
            ft.Container(height=4),
            ft.Text(label, size=10, color=color, weight=ft.FontWeight.W_600),
            ft.Container(height=18),
            form_field(
                "CONFIRMAR",
                confirm_v,
                on_confirm,
                "Repita a nova senha",
                password=True,
                can_reveal_password=True,
                **shared,
            ),
            ft.Container(height=8),
            ft.Text(
                "As senhas não coincidem." if mismatch else "",
                size=11,
                color="#EF4444",
            ),
        ],
        spacing=0,
    )


@ft.component
def StepSuccess(state: AuthRecoveryState) -> ft.Control:
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
                        "Senha redefinida.",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=T,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        f"Pode usar a nova senha para entrar em {state.email or 'sua conta'}.",
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
def AuthRecoveryWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: CompleteCallback | None = None,
    mock: bool = False,
) -> ft.Control:
    """Wizard público de recuperação — 3 steps + sucesso, reativo a `theme`.

    `mock=True` (modo gallery) inicializa com `AUTH_RECOVERY` e abre no
    último step de dados (Nova senha).
    """

    initial = (
        AuthRecoveryState(
            theme=theme,
            step=AuthRecoveryState.TOTAL_STEPS - 1,
            **AUTH_RECOVERY,
        )
        if mock
        else AuthRecoveryState(theme=theme)
    )
    state, _ = ft.use_state(initial)
    if state.theme != theme:
        state.theme = theme

    async def _adapt(s: AuthRecoveryState) -> None:
        if on_complete is None:
            return
        result = on_complete({"email": s.email})
        if inspect.isawaitable(result):
            await result

    return WizardFrame(
        state=state,
        step_labels=["E-mail", "Código", "Nova senha"],
        step_hints=["Identificação", "Verificação", "Definir nova"],
        steps=[StepEmailRecovery, StepCodigo, StepNovaSenha, StepSuccess],
        on_complete=_adapt,
        last_step_label="Concluir",
        loading_label="Salvando...",
    )
