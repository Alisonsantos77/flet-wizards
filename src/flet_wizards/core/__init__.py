"""API pública do core: estado, tema, componentes, frame, registro, guard."""

from .base_state import BaseWizardState
from .base_wizard import NavBar, Sidebar, WizardFrame
from .components import divider, form_field, ghost_button, primary_button
from .platform_guard import PlatformGuard
from .registry import (
    WizardMeta,
    all_wizards,
    by_category,
    by_id,
    categories,
    register,
)
from .snack import SnackHost, show_error, show_info, show_success
from .theme import (
    DEFAULT_THEME,
    THEME_PAIRS,
    THEMES_BY_NAME,
    WizardTheme,
    resolve_theme,
)

__all__ = [
    "BaseWizardState",
    "DEFAULT_THEME",
    "NavBar",
    "PlatformGuard",
    "Sidebar",
    "SnackHost",
    "THEME_PAIRS",
    "THEMES_BY_NAME",
    "WizardFrame",
    "WizardMeta",
    "WizardTheme",
    "all_wizards",
    "by_category",
    "by_id",
    "categories",
    "divider",
    "form_field",
    "ghost_button",
    "primary_button",
    "register",
    "resolve_theme",
    "show_error",
    "show_info",
    "show_success",
]
