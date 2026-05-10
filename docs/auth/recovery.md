# AuthRecoveryWizard

Recuperação de senha em **3 steps de dados + tela de sucesso**, com código de 6 dígitos e indicador de força animado.

- **ID:** `auth.recovery`
- **Categoria:** `auth`
- **Módulo:** `flet_wizards.auth.recovery`
- **Importação pública:** `from flet_wizards import AuthRecoveryWizard`

---

## Descrição

Fluxo padrão "esqueci minha senha": pede o e-mail, recebe um código de 6 dígitos (entrada em 6 campos individuais) e exige uma nova senha com indicador de força em tempo real (5 níveis). O `on_complete` recebe apenas o `email` — código e senha ficam no `state` interno e nunca são expostos.

Helpers internos `_get_digit` / `_set_digit` armazenam o código como uma string padded com espaços (`PAD_CHAR = " "`), o que permite tratar cada posição independentemente sem mexer no comprimento.

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **E-mail** | Campo de e-mail + instrução de envio do código. |
| 1 | **Código** | 6 campos individuais (`max_length=1`, 48×56px, centro alinhado). |
| 2 | **Nova senha** | Nova senha + indicador de força animado + confirmação. |
| 3 | **Sucesso** | "Senha redefinida." + e-mail destacado. |

---

## Campos por step

### Step 0 — E-mail

| Campo | Tipo | UI |
|---|---|---|
| `email` | `str` | `form_field("E-MAIL", ..., "voce@exemplo.com")` |

### Step 1 — Código

| Campo | Tipo | UI |
|---|---|---|
| `code` | `str` (até 6 chars) | 6 `ft.TextField` em row, cada um com `max_length=1`. |

A leitura/escrita por posição é feita via `_get_digit(code, i)` e `_set_digit(current, i, raw)`.

### Step 2 — Nova senha

| Campo | Tipo | UI |
|---|---|---|
| `new_password` | `str` | `form_field("NOVA SENHA", ..., password=True, can_reveal_password=True)` |
| `confirm_password` | `str` | `form_field("CONFIRMAR", ..., password=True, can_reveal_password=True)` |

Logo abaixo do campo `NOVA SENHA` há uma barra de força (4px de altura, animada via `ft.Animation(300, EASE_OUT_CUBIC)`). Os 5 níveis vêm de `_strength()`:

| Score | Label | Cor | % |
|---|---|---|---|
| 0 | Muito fraca | `#EF4444` | 20% |
| 1 | Fraca | `#F59E0B` | 40% |
| 2 | Razoável | `#FACC15` | 60% |
| 3 | Boa | `#84CC16` | 80% |
| 4 | Forte | `#22C55E` | 100% |

Critérios somados em `score`: `len ≥ 8`, `len ≥ 12`, mistura de letras+dígitos, presença de símbolo (`!@#$%^&*()-_+=[]{}|;:,.<>?/`).

Aviso "As senhas não coincidem." aparece quando `confirm_password` diverge de `new_password`.

### Step 3 — Sucesso

Check (72px) + "Senha redefinida." + "Pode usar a nova senha para entrar em {email}." + botão "Voltar ao início".

---

## Plataformas suportadas

```python
[
    ft.PagePlatform.WINDOWS,
    ft.PagePlatform.MACOS,
    ft.PagePlatform.LINUX,
    ft.PagePlatform.ANDROID,
    ft.PagePlatform.IOS,
]
```

---

## Retorno do `on_complete`

```python
{"email": str}
```

Schema declarado em `META.on_complete_schema = {"email": "str"}`. Código e nova senha ficam apenas no state — quem usa é responsável por validar o código no backend antes de chamar este wizard, ou capturar via componente externo.

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import AuthRecoveryWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_recovery(data: dict) -> None:
        email = data["email"]
        # disparar reset no backend usando email...

    return AuthRecoveryWizard(
        theme=WizardTheme.ROSE,
        on_complete=handle_recovery,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.bgcolor = "#0B0B0F"
    page.render(App)


ft.run(main)
```

---

## Mock no gallery

`flet_wizards.core.mock_data.AUTH_RECOVERY`:

```python
AUTH_RECOVERY = {
    "email": "dev@exemplo.com",
    "code": "429731",
    "new_password": "NovaSenha@123",
    "confirm_password": "NovaSenha@123",
}
```

Em modo mock o wizard abre no step 2 (Nova senha) com a barra de força em "Forte" (verde) e ambos os campos preenchidos.
