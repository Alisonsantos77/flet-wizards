"""AuthLoginWizard — login clássico em e-mail + senha (2 steps + sucesso).

Steps:
  0 — Acesso: e-mail e senha (com revelar)
  1 — Confirmação: card resumo com avatar de iniciais
  2 — Sucesso: confirmação visual + reset

`on_complete` recebe um `dict` no formato declarado em `META.on_complete_schema`:
`{"email": str}`. Aceita callback síncrono ou awaitable.
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
from wizards.core.mock_data import AUTH_LOGIN

META = register(
    WizardMeta(
        id="auth.login",
        name="Login Clássico",
        category="auth",
        description="Wizard de autenticação com e-mail e senha em dois steps.",
        steps=["Acesso", "Confirmação"],
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


@ft.observable
@dataclass
class AuthLoginState(BaseWizardState):
    """Store reativo do AuthLoginWizard."""

    TOTAL_STEPS: ClassVar[int] = 2

    email: str = ""
    password: str = ""

    def reset(self) -> None:
        super().reset()
        self.email = ""
        self.password = ""


@ft.component
def StepAcesso(state: AuthLoginState) -> ft.Control:
    """Captura de credenciais — padrão híbrido use_state + estado global."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    email_v, set_email = ft.use_state(state.email)
    pass_v, set_pass = ft.use_state(state.password)

    def on_email(e):
        set_email(e.control.value)
        state.email = e.control.value

    def on_pass(e):
        set_pass(e.control.value)
        state.password = e.control.value

    shared = dict(primary=P, text=T, sub=S, card=C, border=B)

    return ft.Column(
        [
            ft.Text(
                "Bem-vindo de volta",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Acesse sua conta com e-mail e senha.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            form_field(
                "E-MAIL",
                email_v,
                on_email,
                "voce@exemplo.com",
                **shared,
            ),
            ft.Container(height=18),
            form_field(
                "SENHA",
                pass_v,
                on_pass,
                "••••••••",
                password=True,
                can_reveal_password=True,
                **shared,
            ),
        ],
        spacing=0,
    )


@ft.component
def StepConfirmacao(state: AuthLoginState) -> ft.Control:
    """Card de revisão — botão de confirmação fica na NavBar."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    SX = state.surface()

    initial = (state.email[:1] or "?").upper()

    avatar = ft.Container(
        width=56,
        height=56,
        border_radius=28,
        bgcolor=P,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            initial,
            size=22,
            color="#FFFFFF",
            weight=ft.FontWeight.BOLD,
        ),
    )

    return ft.Column(
        [
            ft.Text("Tudo certo?", size=22, weight=ft.FontWeight.BOLD, color=T),
            ft.Container(height=4),
            ft.Text(
                "Confirme as credenciais antes de entrar.",
                size=13,
                color=S,
            ),
            ft.Container(height=24),
            ft.Container(
                bgcolor=SX,
                padding=ft.Padding.all(20),
                border_radius=10,
                border=ft.Border.all(1, B),
                content=ft.Row(
                    [
                        avatar,
                        ft.Container(width=16),
                        ft.Column(
                            [
                                ft.Text(
                                    state.email or "—",
                                    size=14,
                                    color=T,
                                    weight=ft.FontWeight.W_600,
                                ),
                                ft.Container(height=2),
                                ft.Text(
                                    "Pronto para entrar.",
                                    size=12,
                                    color=S,
                                ),
                            ],
                            spacing=0,
                            expand=1,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        ],
        spacing=0,
    )


@ft.component
def StepSuccess(state: AuthLoginState) -> ft.Control:
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
                        f"Bem-vindo, {state.email or 'visitante'}.",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=T,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Login realizado com sucesso.",
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
def AuthLoginWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: CompleteCallback | None = None,
    mock: bool = False,
) -> ft.Control:
    """Wizard público de login — 2 steps + sucesso, reativo a `theme`.

    `mock=True` (modo gallery) inicializa o state com `AUTH_LOGIN` e abre
    direto no último step de dados (Confirmação) como preview rápido.
    """

    initial = (
        AuthLoginState(
            theme=theme,
            step=AuthLoginState.TOTAL_STEPS - 1,
            **AUTH_LOGIN,
        )
        if mock
        else AuthLoginState(theme=theme)
    )
    state, _ = ft.use_state(initial)
    if state.theme != theme:
        state.theme = theme

    async def _adapt(s: AuthLoginState) -> None:
        if on_complete is None:
            return
        result = on_complete({"email": s.email})
        if inspect.isawaitable(result):
            await result

    return WizardFrame(
        state=state,
        step_labels=["Acesso", "Confirmação"],
        step_hints=["E-mail e senha", "Revisar e entrar"],
        steps=[StepAcesso, StepConfirmacao, StepSuccess],
        on_complete=_adapt,
        last_step_label="Entrar",
        loading_label="Entrando...",
    )
