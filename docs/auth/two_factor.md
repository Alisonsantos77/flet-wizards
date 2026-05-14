# AuthTwoFactorWizard

Verificação em 2 fatores mobile-first em **1 step de dados + tela de sucesso**, com 6 campos individuais de dígito e fundo geométrico decorativo.

- **ID:** `auth.two_factor`
- **Categoria:** `auth`
- **Módulo:** `flet_wizards.auth.two_factor`
- **Importação pública:** `from flet_wizards import AuthTwoFactorWizard`

---

## Descrição

Coleta um código de 6 dígitos digitado pelo usuário (tipicamente vindo de um app autenticador como Google Authenticator, Authy, 1Password). Validação local exige os 6 dígitos preenchidos antes de avançar. O fundo decorativo é uma malha geométrica de pontos e anéis renderizada via `ft.Stack` (sem dependência de imagens externas — mantém o pacote leve).

`on_complete` recebe `{"code": str}` — a aplicação cliente é responsável por validar o código contra o backend. A lib não conhece o backend, apenas entrega o código digitado.

---

## Quando usar

- Verificação de identidade após login em aplicações sensíveis (banking, saúde, admin).
- Confirmação de ações críticas (transferência, exclusão de conta).
- Adição de novo dispositivo confiável.

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **Código** | Escudo + 6 `TextField` individuais (`max_length=1`, `keyboard_type=NUMBER`) + nota de expiração. |
| 1 | **Sucesso** | Escudo grande, "Identidade confirmada" e botão de reset. |

---

## Campos coletados

| Campo | Tipo | Descrição |
|---|---|---|
| `code` | `str` | Buffer de 6 caracteres armazenado padded com espaços (`PAD_CHAR = " "`); helpers `_get_digit` e `_set_digit` manejam por posição. |

---

## Parâmetros

| Parâmetro | Tipo | Default | Descrição |
|---|---|---|---|
| `theme` | `WizardTheme` | `WizardTheme.SLATE` | Paleta visual. |
| `on_complete` | `Callable[[dict], Any] \| None` | `None` | Callback recebendo `{"code": str}`. |
| `mock` | `bool` | `False` | Preview no gallery — inicializa com `AUTH_TWO_FACTOR`. |

---

## Plataformas suportadas

```python
[ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
```

Em desktop, o `PlatformGuard` exibe modal com botão "Continuar mesmo assim".

---

## Retorno do `on_complete`

```python
{"code": str}
```

Schema declarado em `META.on_complete_schema = {"code": "str"}`.

---

## Limitações conhecidas

- **Sem auto-advance entre dígitos.** Auto-advance via `on_change` foi removido temporariamente em 0.2.1 e ainda não foi reintroduzido. O usuário precisa tocar manualmente em cada campo.
- **Botão "Reenviar código" é placeholder.** Ele apenas dispara um `show_info` informando que reenvio é responsabilidade do app consumidor — não há callback exposto para integrar com backend.
- **Contagem "expira em 30 segundos" é texto fixo.** Não há countdown real nem `on_expire` hook.
- **Sem validação de formato.** Qualquer caractere passa por digit_field — a validação numérica vem só do `keyboard_type=NUMBER` no teclado virtual mobile.

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import AuthTwoFactorWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_2fa(data: dict) -> None:
        code = data["code"]
        # validar contra backend...

    return AuthTwoFactorWizard(
        theme=WizardTheme.SLATE,
        on_complete=handle_2fa,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.bgcolor = "#0B0B0F"
    page.render(App)


ft.run(main)
```

---

## Mock no gallery

`flet_wizards.core.mock_data.AUTH_TWO_FACTOR`:

```python
AUTH_TWO_FACTOR = {"code": "318274"}
```

Em modo mock o wizard abre no step 0 já com os 6 dígitos preenchidos para servir de preview rápido.
