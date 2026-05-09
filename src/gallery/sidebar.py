"""Sidebar — navegação lateral por categoria.

Usa `categories()` e `by_category()` do registry para descobrir templates
dinamicamente. Cada categoria é um header clicável (navega para `/<cat>`,
mostrando o grid). Cada template é uma row clicável (navega para
`/<cat>/<id>`, mostrando o wizard com mock=True).

Item ativo destacado com `primary` do tema corrente, detectado via
`use_route_location()`.
"""

import flet as ft

from wizards.core import WizardMeta, by_category, categories

from . import state

SIDEBAR_W = 220


def _meta_path(meta: WizardMeta) -> str:
    """Converte 'auth.login' em '/auth/login'."""
    return "/" + meta.id.replace(".", "/", 1)


def _category_path(category: str) -> str:
    """Converte 'auth' em '/auth'."""
    return f"/{category}"


@ft.component
def Sidebar() -> ft.Control:
    """Coluna esquerda fixa com seções e rows clicáveis."""

    T = state.theme
    location = ft.use_route_location()

    def go_to(path: str):
        async def handler(_e):
            await ft.context.page.push_route(path)

        return handler

    def category_header(cat: str) -> ft.GestureDetector:
        active = location == _category_path(cat)
        return ft.GestureDetector(
            on_tap=go_to(_category_path(cat)),
            content=ft.Container(
                content=ft.Text(
                    cat.upper(),
                    size=10,
                    color=T.primary if active else T.sub,
                    weight=ft.FontWeight.W_700,
                    style=ft.TextStyle(letter_spacing=1.2),
                ),
                padding=ft.Padding.symmetric(horizontal=18, vertical=10),
            ),
        )

    def template_row(meta: WizardMeta) -> ft.GestureDetector:
        path = _meta_path(meta)
        active = location == path
        return ft.GestureDetector(
            on_tap=go_to(path),
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            width=3,
                            height=18,
                            bgcolor=T.primary if active else "transparent",
                            border_radius=2,
                        ),
                        ft.Container(width=8),
                        ft.Text(
                            meta.name,
                            size=13,
                            color=T.text if active else T.sub,
                            weight=ft.FontWeight.W_600
                            if active
                            else ft.FontWeight.W_400,
                        ),
                    ],
                    spacing=0,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=T.card if active else "transparent",
                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                border_radius=6,
                animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT_CUBIC),
            ),
        )

    blocks: list[ft.Control] = []
    for i, cat in enumerate(categories()):
        if i > 0:
            blocks.append(ft.Container(height=14))
        blocks.append(category_header(cat))
        blocks.append(ft.Container(height=4))
        for meta in by_category(cat):
            blocks.append(
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=10),
                    content=template_row(meta),
                )
            )
            blocks.append(ft.Container(height=2))

    return ft.Container(
        width=SIDEBAR_W,
        bgcolor=T.panel,
        border=ft.Border.only(right=ft.BorderSide(1, T.border)),
        padding=ft.Padding.symmetric(vertical=18),
        content=ft.Column(
            [
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=18),
                    content=ft.Text(
                        "flet-wizards",
                        size=14,
                        color=T.text,
                        weight=ft.FontWeight.BOLD,
                    ),
                ),
                ft.Container(height=20),
                *blocks,
                ft.Container(expand=1),
            ],
            spacing=0,
            expand=True,
        ),
    )
