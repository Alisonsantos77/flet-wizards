# flet-wizards

Gallery de templates de wizard multi-step para Flet, prontos para reuso.

## Templates disponíveis

| Categoria | Nome | Steps | Descrição |
|-----------|------|-------|-----------|
| auth | [Login Clássico](docs/auth/login.md) | 2 | Wizard de login com e-mail e senha em dois steps. |
| auth | [Recuperar Senha](docs/auth/recovery.md) | 3 | Wizard de recuperação de senha com código de verificação. |
| auth | [Cadastro](docs/auth/register.md) | 3 | Wizard de cadastro com conta, perfil e confirmação. |
| profile | [Avatar](docs/profile/avatar.md) | 3 | Wizard de configuração de avatar com 3 origens (arquivo, URL, iniciais). |
| profile | [Editar Perfil](docs/profile/edit.md) | 3 | Wizard de edição de perfil com diff visual no resumo. |
| profile | [Setup de Perfil](docs/profile/setup.md) | 3 | Wizard de onboarding com identidade, interesses e preferências. |

## Uso rápido

```python
import flet as ft
from wizards.auth.login import AuthLoginWizard

async def main(page: ft.Page):
    page.render(lambda: AuthLoginWizard(on_complete=lambda d: print(d)))

ft.run(main)
```

## Gallery

```powershell
uv run flet run
```

Abre o showcase com sidebar por categoria, seletor de tema (4 paletas) e preview ao vivo de cada template.

---

_Documentação regenerada automaticamente por `pipeline/cocoindex_pipeline.py`._
