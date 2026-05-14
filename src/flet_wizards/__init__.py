"""flet-wizards — templates de wizard multi-step para Flet.

API pública: as classes de wizard prontas para uso + `WizardTheme`.
Importação direta a partir do package raiz, sem precisar conhecer a
sub-estrutura interna (`auth/`, `profile/`, `onboarding/`, `survey/`, `core/`):

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
from flet_wizards.auth.two_factor import AuthTwoFactorWizard
from flet_wizards.core.theme import WizardTheme
from flet_wizards.onboarding.walkthrough import OnboardingWalkthroughWizard
from flet_wizards.profile.avatar import ProfileAvatarWizard
from flet_wizards.profile.edit import ProfileEditWizard
from flet_wizards.profile.setup import ProfileSetupWizard
from flet_wizards.survey.feedback import SurveyFeedbackWizard

__all__ = [
    "AuthLoginWizard",
    "AuthRegisterWizard",
    "AuthRecoveryWizard",
    "AuthTwoFactorWizard",
    "OnboardingWalkthroughWizard",
    "ProfileSetupWizard",
    "ProfileEditWizard",
    "ProfileAvatarWizard",
    "SurveyFeedbackWizard",
    "WizardTheme",
]

__version__ = "0.2.2"
