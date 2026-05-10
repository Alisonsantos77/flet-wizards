# AuthLoginWizard

Login clássico em **2 steps de dados + tela de sucesso**, com avatar de iniciais no card de revisão.

- **ID:** `auth.login`
- **Categoria:** `auth`
- **Módulo:** `flet_wizards.auth.login`
- **Importação pública:** `from flet_wizards import AuthLoginWizard`

---

## Descrição

Captura e-mail e senha, mostra um card resumo com avatar de iniciais e dispara `on_complete({"email": ...})` quando o usuário confirma. A senha é tratada apenas em memória dentro do `state` — o wizard nunca expõe a senha no callback.

A tela de sucesso (`step == TOTAL_STEPS`) cumprimenta o usuário com a primeira letra do e-mail e oferece um botão "Voltar ao início" que reseta o state.

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **Acesso** | E-mail + senha (com `can_reveal_password=True`). |
| 1 | **Confirmação** | Card resumo com avatar de iniciais + e-mail; botão "Entrar" fica na NavBar. |
| 2 | **Sucesso** | Check verde, "Bem-vindo, …" e botão "Voltar ao início". |

---

## Campos por step

### Step 0 — Acesso

| Campo | Tipo | UI |
|---|---|---|
| `email` | `str` | `form_field("E-MAIL", ..., placeholder="voce@exemplo.com")` |
| `password` | `str` | `form_field("SENHA", ..., password=True, can_reveal_password=True)` |

### Step 1 — Confirmação

Não captura novos dados; renderiza um card com:

- Avatar circular (56px) com a inicial do e-mail
- E-mail
- Texto "Pronto para entrar."

### Step 2 — Sucesso

Renderiza um check (72px) e o nome do usuário; botão "Voltar ao início" chama `state.reset()`.

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

> ⚠️ `ft.PagePlatform` não tem `WEB` no Flet 0.85+. Para detectar browser use `page.web` (boolean) — todos os wizards atuais funcionam normalmente em web.

---

## Retorno do `on_complete`

```python
{"email": str}
```

Schema declarado em `META.on_complete_schema = {"email": "str"}`. Aceita callback síncrono ou awaitable; o wizard chama `inspect.isawaitable(result)` antes de `await`.

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import AuthLoginWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_login(data: dict) -> None:
        email = data["email"]
        # autenticar...

    return AuthLoginWizard(
        theme=WizardTheme.SLATE,
        on_complete=handle_login,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.bgcolor = "#0B0B0F"
    page.render(App)


ft.run(main)
```

---

## Mock no gallery

`flet_wizards.core.mock_data.AUTH_LOGIN`:

```python
AUTH_LOGIN = {
    "email": "dev@exemplo.com",
    "password": "Senha@123",
}
```

Em modo mock o wizard inicializa com esses valores e abre direto no step 1 (Confirmação) como preview rápido. O dev pode navegar para o step 0 clicando em "Voltar".
