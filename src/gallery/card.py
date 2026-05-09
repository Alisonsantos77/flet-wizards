"""WizardCard — card de template usado nas grids de categoria.

Mostra: nome, descrição curta, badge de plataforma, contagem de steps,
e botão "Visualizar" que navega para `/<categoria>/<id>`. O id da meta
é `categoria.template` (ex: "auth.login"); convertido para o path
`/auth/login` na navegação.

Dropa o GIF de preview por enquanto — fica como TODO até ter os assets.
"""

import flet as ft

from wizards.core import WizardMeta

from . import state


def _meta_path(meta: WizardMeta) -> str:
    """Converte 'auth.login' em '/auth/login'."""
    return "/" + meta.id.replace(".", "/", 1)


def _platform_badge_text(meta: WizardMeta) -> str:
    """Texto curto resumindo plataformas suportadas."""
    n = len(meta.platforms)
    if n >= 5:
        return "Todas as plataformas"
    return f"{n} plataforma{'s' if n != 1 else ''}"


@ft.component
def WizardCard(meta: WizardMeta) -> ft.Control:
    """Card de template clicável — botão Visualizar navega para o wizard."""

    T = state.theme

    async def visualize(_e):
        await ft.context.page.push_route(_meta_path(meta))

    badge = ft.Container(
        content=ft.Text(
            _platform_badge_text(meta),
            size=10,
            color=T.accent,
            weight=ft.FontWeight.W_600,
        ),
        border=ft.Border.all(1, T.accent + "60"),
        border_radius=20,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
    )

    steps_badge = ft.Container(
        content=ft.Text(
            f"{len(meta.steps)} steps",
            size=10,
            color=T.sub,
            weight=ft.FontWeight.W_600,
        ),
        bgcolor=T.surface,
        border_radius=20,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
    )

    visualize_btn = ft.GestureDetector(
        on_tap=visualize,
        content=ft.Container(
            content=ft.Text(
                "Visualizar →",
                size=12,
                color="#FFFFFF",
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=T.primary,
            padding=ft.Padding.symmetric(horizontal=18, vertical=10),
            border_radius=8,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
        ),
    )

    preview_placeholder = ft.Container(
        height=120,
        bgcolor=T.surface,
        border_radius=8,
        border=ft.Border.all(1, T.border),
        alignment=ft.Alignment(0, 0),
        content=ft.Text(
            meta.name[:1].upper(),
            size=48,
            color=T.primary,
            weight=ft.FontWeight.BOLD,
        ),
    )

    return ft.Container(
        bgcolor=T.card,
        padding=ft.Padding.all(16),
        border_radius=10,
        border=ft.Border.all(1, T.border),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT_CUBIC),
        content=ft.Column(
            [
                preview_placeholder,
                ft.Container(height=14),
                ft.Text(
                    meta.name,
                    size=15,
                    color=T.text,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=4),
                ft.Text(
                    meta.description,
                    size=12,
                    color=T.sub,
                    max_lines=2,
                ),
                ft.Container(height=12),
                ft.Row([badge, steps_badge], spacing=6),
                ft.Container(height=14),
                ft.Row(
                    [ft.Container(expand=1), visualize_btn],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=0,
        ),
    )
