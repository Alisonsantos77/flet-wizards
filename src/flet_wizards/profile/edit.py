"""ProfileEditWizard — edição de perfil em 3 steps com diff visual.

Steps:
  0 — Dados: nome + e-mail + telefone (pré-populados via initial_data)
  1 — Segurança: senha atual + nova + confirmação
  2 — Confirmar: diff visual destacando apenas campos alterados
  3 — Sucesso

State: name, email, phone, current_password, new_password, confirm.
Adicionalmente armazena `initial_data` (frozen snapshot) para o diff.
`on_complete` recebe `{"changed_fields": dict}` apenas com os campos
modificados (ignorando senhas em texto plano).

`mock=True` simula uma edição: `initial_data` é uma cópia de `PROFILE_EDIT`
e o state aplica uma alteração em `phone` para que a tela de diff tenha
algo para mostrar. Abre no step 2 (Confirmar).
"""

import inspect
from dataclasses import dataclass, field
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
from flet_wizards.core.mock_data import PROFILE_EDIT

META = register(
    WizardMeta(
        id="profile.edit",
        name="Editar Perfil",
        category="profile",
        description="Wizard de edição de perfil com diff visual no resumo.",
        steps=["Dados", "Segurança", "Confirmar"],
        platforms=[
            ft.PagePlatform.WINDOWS,
            ft.PagePlatform.MACOS,
            ft.PagePlatform.LINUX,
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
        ],
        on_complete_schema={"changed_fields": "dict"},
    )
)

VISIBLE_FIELDS: list[tuple[str, str]] = [
    ("name", "Nome"),
    ("email", "E-mail"),
    ("phone", "Telefone"),
]


@ft.observable
@dataclass
class ProfileEditState(BaseWizardState):
    """Store reativo do ProfileEditWizard."""

    TOTAL_STEPS: ClassVar[int] = 3

    name: str = ""
    email: str = ""
    phone: str = ""
    current_password: str = ""
    new_password: str = ""
    confirm: str = ""

    initial_data: dict = field(default_factory=dict)

    def reset(self) -> None:
        super().reset()
        for k, v in self.initial_data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.current_password = ""
        self.new_password = ""
        self.confirm = ""


def _changed_fields(state: ProfileEditState) -> dict:
    """Devolve {field: novo_valor} apenas para campos visíveis modificados."""
    current = {"name": state.name, "email": state.email, "phone": state.phone}
    changed = {}
    for key, _ in VISIBLE_FIELDS:
        if state.initial_data.get(key, "") != current[key]:
            changed[key] = current[key]
    if state.new_password and state.new_password != state.initial_data.get(
        "new_password", ""
    ):
        changed["password"] = "updated"
    return changed


@ft.component
def StepDados(state: ProfileEditState) -> ft.Control:
    """Edição de nome, e-mail e telefone."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    name_v, set_name = ft.use_state(state.name)
    email_v, set_email = ft.use_state(state.email)
    phone_v, set_phone = ft.use_state(state.phone)

    def on_name(e):
        set_name(e.control.value)
        state.name = e.control.value

    def on_email(e):
        set_email(e.control.value)
        state.email = e.control.value

    def on_phone(e):
        set_phone(e.control.value)
        state.phone = e.control.value

    shared = dict(primary=P, text=T, sub=S, card=C, border=B)

    return ft.Column(
        [
            ft.Text(
                "Atualize seus dados",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Modifique apenas o que precisar — o resumo destacará as mudanças.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            form_field("NOME", name_v, on_name, "Nome completo", **shared),
            ft.Container(height=18),
            form_field("E-MAIL", email_v, on_email, "voce@exemplo.com", **shared),
            ft.Container(height=18),
            form_field(
                "TELEFONE",
                phone_v,
                on_phone,
                "+55 11 90000-0000",
                **shared,
            ),
        ],
        spacing=0,
    )


@ft.component
def StepSeguranca(state: ProfileEditState) -> ft.Control:
    """Atualização opcional de senha — atual + nova + confirmação."""

    P = state.primary()
    T = state.text()
    S = state.sub()
    B = state.border()
    C = state.card()

    cur_v, set_cur = ft.use_state(state.current_password)
    new_v, set_new = ft.use_state(state.new_password)
    confirm_v, set_confirm = ft.use_state(state.confirm)

    def on_cur(e):
        set_cur(e.control.value)
        state.current_password = e.control.value

    def on_new(e):
        set_new(e.control.value)
        state.new_password = e.control.value

    def on_confirm(e):
        set_confirm(e.control.value)
        state.confirm = e.control.value

    shared = dict(primary=P, text=T, sub=S, card=C, border=B)
    mismatch = bool(confirm_v) and bool(new_v) and confirm_v != new_v

    return ft.Column(
        [
            ft.Text(
                "Segurança",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                "Deixe em branco para manter a senha atual.",
                size=13,
                color=S,
            ),
            ft.Container(height=28),
            form_field(
                "SENHA ATUAL",
                cur_v,
                on_cur,
                "Necessária para alterar",
                password=True,
                can_reveal_password=True,
                **shared,
            ),
            ft.Container(height=18),
            form_field(
                "NOVA SENHA",
                new_v,
                on_new,
                "Mínimo 8 caracteres",
                password=True,
                can_reveal_password=True,
                **shared,
            ),
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
def StepConfirmarEdit(state: ProfileEditState) -> ft.Control:
    """Diff visual: lista apenas os campos alterados, com old → new."""

    T = state.text()
    S = state.sub()
    B = state.border()
    SX = state.surface()

    initial = state.initial_data
    diff: list[tuple[str, str, str]] = []
    for key, label in VISIBLE_FIELDS:
        old = initial.get(key, "") or "—"
        new = getattr(state, key) or "—"
        if old != new:
            diff.append((label, old, new))

    pwd_changed = bool(state.new_password) and state.new_password != initial.get(
        "new_password", ""
    )
    if pwd_changed:
        diff.append(("Senha", "•••", "atualizada"))

    def diff_row(label: str, old: str, new: str) -> ft.Container:
        return ft.Container(
            bgcolor=SX,
            padding=ft.Padding.all(14),
            border_radius=8,
            border=ft.Border.all(1, B),
            content=ft.Column(
                [
                    ft.Text(
                        label,
                        size=10,
                        color=S,
                        weight=ft.FontWeight.W_500,
                        style=ft.TextStyle(letter_spacing=0.8),
                    ),
                    ft.Container(height=6),
                    ft.Row(
                        [
                            ft.Text(
                                old,
                                size=12,
                                color=S,
                                italic=True,
                            ),
                            ft.Text("→", size=12, color=S),
                            ft.Text(
                                new,
                                size=14,
                                color=T,
                                weight=ft.FontWeight.W_600,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=0,
            ),
        )

    if not diff:
        return ft.Column(
            [
                ft.Text(
                    "Nada a alterar",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=T,
                ),
                ft.Container(height=4),
                ft.Text(
                    "Nenhum campo foi modificado em relação ao original.",
                    size=13,
                    color=S,
                ),
            ],
            spacing=0,
        )

    return ft.Column(
        [
            ft.Text(
                "Alterações pendentes",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=T,
            ),
            ft.Container(height=4),
            ft.Text(
                f"{len(diff)} campo(s) serão atualizado(s).",
                size=13,
                color=S,
            ),
            ft.Container(height=24),
            *[
                ft.Column([diff_row(*item), ft.Container(height=10)], spacing=0)
                for item in diff
            ],
        ],
        spacing=0,
    )


@ft.component
def StepSuccess(state: ProfileEditState) -> ft.Control:
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
                        "Perfil atualizado.",
                        size=18,
                        weight=ft.FontWeight.W_500,
                        color=T,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Suas alterações foram salvas com sucesso.",
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
def ProfileEditWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: CompleteCallback | None = None,
    mock: bool = False,
    initial_data: dict | None = None,
) -> ft.Control:
    """Wizard público de edição de perfil — 3 steps + sucesso.

    `initial_data` pré-popula os campos e serve de baseline para o diff.
    `mock=True` simula uma alteração em `phone` para que o diff tenha
    conteúdo na abertura (em step 2). Ignora `initial_data` quando mock.
    """

    if mock:
        snapshot = dict(PROFILE_EDIT)
        modified = dict(snapshot)
        modified["phone"] = "+55 11 99999-8888"
        initial = ProfileEditState(
            theme=theme,
            step=ProfileEditState.TOTAL_STEPS - 1,
            initial_data=snapshot,
            **modified,
        )
    else:
        snapshot = dict(initial_data or {})
        initial = ProfileEditState(
            theme=theme,
            initial_data=snapshot,
            **{k: v for k, v in snapshot.items() if k not in ("initial_data",)},
        )

    state, _ = ft.use_state(initial)
    if state.theme != theme:
        state.theme = theme

    async def _adapt(s: ProfileEditState) -> None:
        if on_complete is None:
            logger.warning(
                "[ProfileEditWizard]: on_complete não fornecido — wizard funcionará como demo"
            )
            return
        result = on_complete({"changed_fields": _changed_fields(s)})
        if inspect.isawaitable(result):
            await result

    return WizardFrame(
        state=state,
        step_labels=["Dados", "Segurança", "Confirmar"],
        step_hints=["Identificação", "Senha", "Resumo das mudanças"],
        steps=[StepDados, StepSeguranca, StepConfirmarEdit, StepSuccess],
        on_complete=_adapt,
        last_step_label="Salvar alterações",
        loading_label="Salvando...",
    )
