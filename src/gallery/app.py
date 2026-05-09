"""GalleryApp — entrypoint do showcase com `ft.Router`.

Estrutura de rotas (manage_views=False, single tree com outlet):

    /                        → Redirect (use_effect → push_route /auth/login)
    /<categoria>             → CategoryView (grid de cards)
    /<categoria>/<template>  → WizardView (renderiza wizard com mock=True)

`GalleryShell` é o componente layout: Sidebar (full-height) + Header
(top do conteúdo) + outlet (`use_route_outlet`). Toda troca de rota
faz fade no outlet via AnimatedSwitcher com `key=use_route_location()`.

Imports dos 6 wizards no topo são intencionais: cada `import` dispara
o `register(WizardMeta(...))` no módulo, populando o registry usado
pela Sidebar e pelo CategoryView. `WIZARDS_BY_ID` é o dispatch para
renderizar o componente concreto a partir do id da meta.

Estado global de tema vive em `gallery.state` (singleton observável)
— compartilhado pelos 3 componentes via import.
"""

import flet as ft
from loguru import logger

from wizards.auth.login import AuthLoginWizard
from wizards.auth.recovery import AuthRecoveryWizard
from wizards.auth.register import AuthRegisterWizard
from wizards.core import (
    SnackHost,
    THEMES_BY_NAME,
    WizardTheme,
    by_category,
    by_id,
    show_success,
)
from wizards.profile.avatar import ProfileAvatarWizard
from wizards.profile.edit import ProfileEditWizard
from wizards.profile.setup import ProfileSetupWizard

from . import state
from .card import WizardCard
from .sidebar import Sidebar

WIZARDS_BY_ID: dict = {
    "auth.login": AuthLoginWizard,
    "auth.register": AuthRegisterWizard,
    "auth.recovery": AuthRecoveryWizard,
    "profile.setup": ProfileSetupWizard,
    "profile.edit": ProfileEditWizard,
    "profile.avatar": ProfileAvatarWizard,
}


def _success_message(wizard_id: str, data: dict) -> str:
    """Mensagem amigável por wizard para o snack de conclusão."""
    if wizard_id == "auth.login":
        return f"Logado como {data.get('email', '?')}"
    if wizard_id == "auth.register":
        return f"Conta criada para {data.get('name', '?')}"
    if wizard_id == "auth.recovery":
        return f"Senha redefinida para {data.get('email', '?')}"
    if wizard_id == "profile.setup":
        return f"Perfil configurado · {data.get('name', '?')}"
    if wizard_id == "profile.edit":
        changed = data.get("changed_fields", {})
        return f"{len(changed)} campo(s) atualizado(s)"
    if wizard_id == "profile.avatar":
        return f"Avatar salvo · {data.get('source', '?')}"
    return "Concluído"


def _make_handler(wizard_id: str):
    async def handler(data: dict) -> None:
        logger.info("[{}] complete: {}", wizard_id, data)
        show_success(_success_message(wizard_id, data))

    return handler


def _parse_location(location: str) -> tuple[str, str]:
    """('/auth/login') → ('auth', 'login'). Vazio onde faltar."""
    parts = location.strip("/").split("/")
    cat = parts[0] if parts and parts[0] else ""
    tid = parts[1] if len(parts) > 1 else ""
    return cat, tid


@ft.component
def Header() -> ft.Control:
    """Header fixo com título do wizard ativo + 4 swatches de tema."""

    T = state.theme
    location = ft.use_route_location()
    cat, tid = _parse_location(location)

    if cat and tid:
        meta = by_id(f"{cat}.{tid}")
        title = meta.name if meta else "Não encontrado"
        subtitle = meta.description if meta else ""
    elif cat:
        title = f"Templates · {cat.capitalize()}"
        subtitle = "Escolha um template para visualizar"
    else:
        title = "flet-wizards"
        subtitle = ""

    def pick_theme(theme: WizardTheme):
        def handler(_e):
            state.theme = theme

        return handler

    def swatch(_name: str, theme: WizardTheme) -> ft.GestureDetector:
        selected = state.theme is theme
        return ft.GestureDetector(
            on_tap=pick_theme(theme),
            content=ft.Container(
                width=22,
                height=22,
                border_radius=11,
                bgcolor=theme.primary,
                border=ft.Border.all(2, "#FFFFFF" if selected else "transparent"),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
            ),
        )

    return ft.Container(
        bgcolor=T.surface,
        padding=ft.Padding.symmetric(horizontal=28, vertical=14),
        border=ft.Border.only(bottom=ft.BorderSide(1, T.border)),
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            title,
                            size=16,
                            color=T.text,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(subtitle, size=11, color=T.sub) if subtitle else ft.Container(),
                    ],
                    spacing=2,
                    expand=1,
                ),
                *[swatch(name, theme) for name, theme in THEMES_BY_NAME.items()],
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


@ft.component
def Redirect() -> ft.Control:
    """Componente índice — redireciona para /auth/login no mount via use_effect."""

    async def do_redirect():
        await ft.context.page.push_route("/auth/login")

    ft.use_effect(do_redirect)

    return ft.Container(expand=True, bgcolor=state.theme.bg)


@ft.component
def NotFoundView() -> ft.Control:
    """Fallback quando rota não bate com nenhum template registrado."""

    T = state.theme

    return ft.Container(
        expand=True,
        bgcolor=T.bg,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            [
                ft.Text("🔍", size=64),
                ft.Container(height=12),
                ft.Text(
                    "Template não encontrado",
                    size=18,
                    color=T.text,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=6),
                ft.Text(
                    "Use a sidebar para escolher um template existente.",
                    size=13,
                    color=T.sub,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            tight=True,
        ),
    )


@ft.component
def CategoryView() -> ft.Control:
    """Grid de cards dos templates da categoria atual."""

    T = state.theme
    location = ft.use_route_location()
    cat, _ = _parse_location(location)

    metas = by_category(cat)

    if not metas:
        return NotFoundView()

    cards_per_row = 2
    rows: list[ft.Control] = []
    for i in range(0, len(metas), cards_per_row):
        chunk = metas[i : i + cards_per_row]
        cells: list[ft.Control] = []
        for j, meta in enumerate(chunk):
            if j > 0:
                cells.append(ft.Container(width=14))
            cells.append(ft.Container(content=WizardCard(meta), expand=1))
        while len(cells) < cards_per_row * 2 - 1:
            cells.append(ft.Container(width=14))
            cells.append(ft.Container(expand=1))
        rows.append(ft.Row(cells, vertical_alignment=ft.CrossAxisAlignment.START))
        rows.append(ft.Container(height=14))

    return ft.Container(
        expand=True,
        bgcolor=T.bg,
        padding=ft.Padding.all(28),
        content=ft.Column(
            [
                ft.Text(
                    f"{len(metas)} template{'s' if len(metas) != 1 else ''} disponíveis",
                    size=12,
                    color=T.sub,
                ),
                ft.Container(height=18),
                *rows,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        ),
    )


@ft.component
def WizardView() -> ft.Control:
    """Renderiza o wizard cujo id é derivado do route_location atual."""

    T = state.theme
    location = ft.use_route_location()
    cat, tid = _parse_location(location)
    full_id = f"{cat}.{tid}" if cat and tid else ""

    wizard_cls = WIZARDS_BY_ID.get(full_id)
    if wizard_cls is None:
        return NotFoundView()

    return ft.Container(
        expand=True,
        bgcolor=T.bg,
        content=wizard_cls(
            theme=T,
            on_complete=_make_handler(full_id),
            mock=True,
        ),
    )


@ft.component
def GalleryShell() -> ft.Control:
    """Layout pai: SnackHost + Sidebar + (Header + outlet com fade)."""

    T = state.theme
    location = ft.use_route_location()
    outlet = ft.use_route_outlet()

    content_area = ft.AnimatedSwitcher(
        content=ft.Container(
            key=location,
            content=outlet,
            expand=True,
        ),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=240,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_CUBIC,
        switch_out_curve=ft.AnimationCurve.EASE_IN_CUBIC,
        expand=True,
    )

    return ft.Container(
        expand=True,
        bgcolor=T.bg,
        content=ft.Column(
            [
                SnackHost(),
                ft.Row(
                    [
                        Sidebar(),
                        ft.Column(
                            [
                                Header(),
                                ft.Container(expand=True, content=content_area),
                            ],
                            spacing=0,
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            ],
            spacing=0,
            expand=True,
        ),
    )


@ft.component
def GalleryApp() -> ft.Control:
    """Componente raiz — define o ft.Router com o tree de rotas."""

    return ft.Router(
        routes=[
            ft.Route(
                path="/",
                component=GalleryShell,
                children=[
                    ft.Route(index=True, component=Redirect),
                    ft.Route(path="auth", component=CategoryView),
                    ft.Route(path="auth/:tid", component=WizardView),
                    ft.Route(path="profile", component=CategoryView),
                    ft.Route(path="profile/:tid", component=WizardView),
                ],
            ),
        ],
        not_found=NotFoundView,
    )
