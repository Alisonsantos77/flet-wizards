"""Gallery app — showcase estilo Microsoft Store dos wizards.

Expõe `GalleryState` (singleton observável compartilhado entre Sidebar,
Card e GalleryShell para o tema corrente) e re-exporta `GalleryApp`
para o entrypoint em `main.py`.
"""

from dataclasses import dataclass, field

import flet as ft

from wizards.core import WizardTheme


@ft.observable
@dataclass
class GalleryState:
    """Store reativo compartilhado pelo gallery — apenas o tema corrente."""

    theme: WizardTheme = field(default_factory=lambda: WizardTheme.SLATE)


state = GalleryState()
