"""flet-wizards — templates de wizard multi-step para Flet.

API pública: as 6 classes de wizard prontas para uso + `WizardTheme`.
Importação direta a partir do package raiz, sem precisar conhecer a
sub-estrutura interna (`auth/`, `profile/`, `core/`):

```python
from flet_wizards import AuthLoginWizard, WizardTheme

AuthLoginWizard(theme=WizardTheme.SLATE, on_complete=...)
```

Para acessar utilitários internos (registry, snack, base_state),
importe explicitamente do módulo correspondente em `flet_wizards.core`.
"""

from flet_wizards.auth.login import AuthLoginWizard
from flet_wizards.auth.recovery import AuthRecoveryWizard
from flet_wizards.auth.register import AuthRegisterWizard
from flet_wizards.core.theme import WizardTheme
from flet_wizards.profile.avatar import ProfileAvatarWizard
from flet_wizards.profile.edit import ProfileEditWizard
from flet_wizards.profile.setup import ProfileSetupWizard

__all__ = [
    "AuthLoginWizard",
    "AuthRegisterWizard",
    "AuthRecoveryWizard",
    "ProfileSetupWizard",
    "ProfileEditWizard",
    "ProfileAvatarWizard",
    "WizardTheme",
]

__version__ = "0.1.1"
