"""AuthRegisterWizard — cadastro em 3 steps (conta, perfil, confirmação).

Steps:
  0 — Conta: e-mail, senha, confirmação de senha
  1 — Perfil: nome + 6 chips de papel (Dev, Designer, Produto, Marketing, Vendas, Outro)
  2 — Confirmar: card review com avatar de iniciais, nome, papel e e-mail
  3 — Sucesso

State: email, password, confirm_password, name, role.
`on_complete` recebe `{"email": str, "name": str, "role": str}`.

`mock=True` inicializa com `AUTH_REGISTER` e abre no step 2 (Confirmar).
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
from flet_wizards.core.mock_data import AUTH_REGISTER

META = register(
    WizardMeta(
        id="auth.register",
        name="Cadastro",
        category="auth",
        description="Wizard de cadastro com conta, perfil e confirmação.",
        steps=["Conta", "Perfil", "Confirmar"],
        platforms=[
            ft.PagePlatform.WINDOWS,
            ft.PagePlatform.MACOS,
            ft.PagePlatform.LINUX,
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
        ],
        on_complete_schema={"email": "str", "name": "str", "role": "str"},
    )
)

ROLES: list[str] = ["Dev", "Designer", "Produto", "Marketing", "Vendas", "Outro"]


@ft.observable
@dataclass
class AuthRegisterState(BaseWizardState):
    """Store reativo do AuthRegisterWizard."""

    TOTAL_STEPS: ClassVar[int] = 3

    email: str = ""
    password: str = ""
    confirm_password: str = ""
    name: str = ""
    role: str = ""

    def reset(self) -> None:
        super().reset()
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.name = ""
        self.role = ""


def _initials(name: str) -> str:
    parts = [p for p in name.strip().split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][:1] + parts[-1][:1]).upper()


@ft.component
def StepConta(state: AuthRegisterState) -> ft.Control:
    """E-mail, senha e confirmação de senha."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    email_v, set_email = ft.use_state(state.email)
    pass_v, set_pass = ft.use_state(state.password)
    confirm_v, set_confirm = ft.use_state(state.confirm_password)

    def on_email(e):
        set_email(e.control.value)
        state.email = e.control.value

    def on_pass(e):
        set_pass(e.control.value)
        state.password = e.control.value

    def on_confirm(e):
        set_confirm(e.control.value)
        state.confirm_password = e.control.value

    shared = dict(primary=P, text=T, sub=S, card=C, border=B)

    mismatch = (
        confirm_v
        and pass_v
        and confirm_v != pass_v
    )

    return ft.Column(
        [
            ft.Text(
                "Crie sua conta",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Comece informando suas credenciais.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            form_field("E-MAIL", email_v, on_email, "voce@exemplo.com", **shared),
            ft.Container(height=18),
            form_field(
                "SENHA",
                pass_v,
                on_pass,
                "Mínimo 8 caracteres",
                password=True,
                can_reveal_password=True,
                **shared,
            ),
            ft.Container(height=18),
            form_field(
                "CONFIRMAR SENHA",
                confirm_v,
                on_confirm,
                "Repita a senha",
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
def StepPerfil(state: AuthRegisterState) -> ft.Control:
    """Nome + seletor de papel via 6 chips."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    name_v, set_name = ft.use_state(state.name)
    role_v, set_role = ft.use_state(state.role)

    def on_name(e):
        set_name(e.control.value)
        state.name = e.control.value

    def pick_role(label: str):
        set_role(label)
        state.role = label

    def role_chip(label: str) -> ft.GestureDetector:
        sel = role_v == label
        return ft.GestureDetector(
            on_tap=lambda _e, l=label: pick_role(l),
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

    chip_rows = [ROLES[:3], ROLES[3:]]
    shared = dict(primary=P, text=T, sub=S, card=C, border=B)

    return ft.Column(
        [
            ft.Text(
                "Conte sobre você",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Como devemos chamar você e o que você faz.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            form_field("NOME", name_v, on_name, "Nome completo", **shared),
            ft.Container(height=22),
            ft.Text(
                "PAPEL",
                size=11,
                color=S,
                weight=ft.FontWeight.W_500,
                style=ft.TextStyle(letter_spacing=0.8),
            ),
            ft.Container(height=10),
            *[
                ft.Column(
                    [
                        ft.Row([role_chip(r) for r in row], spacing=8),
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
def StepConfirmar(state: AuthRegisterState) -> ft.Control:
    """Card review com avatar, nome (com papel inline) e e-mail."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    SX = state.surface()

    avatar = ft.Container(
        width=64,
        height=64,
        border_radius=32,
        bgcolor=P,
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            _initials(state.name),
            size=22,
            color="#FFFFFF",
            weight=ft.FontWeight.BOLD,
        ),
    )

    display_name = state.name or "Sem nome"
    name_line = (
        f"{display_name} ({state.role})" if state.role else display_name
    )

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
                "Revise os dados antes de criar a conta.",
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
                        ft.Container(width=18),
                        ft.Column(
                            [
                                ft.Text(
                                    name_line,
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=T,
                                ),
                                ft.Container(height=4),
                                ft.Text(
                                    state.email or "—",
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
def StepSuccess(state: AuthRegisterState) -> ft.Control:
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
                        f"Bem-vindo, {state.name.split()[0] if state.name else 'visitante'}.",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=T,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Conta criada com sucesso.",
                        size=13,
                        color=S,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=28),
                    primary_button(
                        "Voltar ao início",
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
def AuthRegisterWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: CompleteCallback | None = None,
    mock: bool = False,
) -> ft.Control:
    """Wizard público de cadastro — 3 steps + sucesso, reativo a `theme`.

    `mock=True` (modo gallery) inicializa com `AUTH_REGISTER` e abre no
    último step de dados (Confirmar).
    """

    initial = (
        AuthRegisterState(
            theme=theme,
            step=AuthRegisterState.TOTAL_STEPS - 1,
            **AUTH_REGISTER,
        )
        if mock
        else AuthRegisterState(theme=theme)
    )
    state, _ = ft.use_state(initial)
    if state.theme != theme:
        state.theme = theme

    async def _adapt(s: AuthRegisterState) -> None:
        if on_complete is None:
            logger.warning(
                "[AuthRegisterWizard]: on_complete não fornecido — wizard funcionará como demo"
            )
            return
        result = on_complete(
            {"email": s.email, "name": s.name, "role": s.role}
        )
        if inspect.isawaitable(result):
            await result

    return WizardFrame(
        state=state,
        step_labels=["Conta", "Perfil", "Confirmar"],
        step_hints=["Credenciais", "Sobre você", "Revisar e criar"],
        steps=[StepConta, StepPerfil, StepConfirmar, StepSuccess],
        on_complete=_adapt,
        last_step_label="Criar conta",
        loading_label="Criando...",
    )
