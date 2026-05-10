# AuthRegisterWizard

Cadastro em **3 steps de dados + tela de sucesso**: conta, perfil e revisão.

- **ID:** `auth.register`
- **Categoria:** `auth`
- **Módulo:** `flet_wizards.auth.register`
- **Importação pública:** `from flet_wizards import AuthRegisterWizard`

---

## Descrição

Coleta credenciais, identidade e papel profissional do usuário em três telas, mostra um card review com avatar de iniciais (ex.: "Ada Lovelace" → "AL") e dispara `on_complete` com `email`, `name` e `role`. Senha e confirmação ficam apenas no `state` interno — não vão para o callback.

Inclui validação inline de senhas que não coincidem ("As senhas não coincidem.") no step 0.

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **Conta** | E-mail + senha + confirmação de senha; alerta se confirmação ≠ senha. |
| 1 | **Perfil** | Nome + 6 chips de papel single-select. |
| 2 | **Confirmar** | Card review: avatar de iniciais, nome, badge de papel e e-mail. |
| 3 | **Sucesso** | Check verde, "Bem-vindo, {primeiro nome}." e botão "Voltar ao início". |

---

## Campos por step

### Step 0 — Conta

| Campo | Tipo | UI |
|---|---|---|
| `email` | `str` | `form_field("E-MAIL", ..., "voce@exemplo.com")` |
| `password` | `str` | `form_field("SENHA", ..., password=True, can_reveal_password=True)` |
| `confirm_password` | `str` | `form_field("CONFIRMAR SENHA", ..., password=True, can_reveal_password=True)` |

### Step 1 — Perfil

| Campo | Tipo | UI |
|---|---|---|
| `name` | `str` | `form_field("NOME", ..., "Nome completo")` |
| `role` | `str` | 6 `GestureDetector` chips: `Dev`, `Designer`, `Produto`, `Marketing`, `Vendas`, `Outro` |

### Step 2 — Confirmar

Apenas leitura. Renderiza:

- Avatar circular (64px) com iniciais derivadas do nome (`"Ada Lovelace"` → `"AL"`, `"Ada"` → `"AD"`)
- Nome do usuário
- Badge com o papel selecionado (estilo accent)
- E-mail

### Step 3 — Sucesso

Check (72px) + "Bem-vindo, {primeiro nome}." + botão "Voltar ao início" → `state.reset()`.

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
{"email": str, "name": str, "role": str}
```

Schema declarado em `META.on_complete_schema = {"email": "str", "name": "str", "role": "str"}`.

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import AuthRegisterWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_register(data: dict) -> None:
        # data == {"email": ..., "name": ..., "role": ...}
        # criar conta...
        ...

    return AuthRegisterWizard(
        theme=WizardTheme.EMERALD,
        on_complete=handle_register,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.bgcolor = "#0B0B0F"
    page.render(App)


ft.run(main)
```

---

## Mock no gallery

`flet_wizards.core.mock_data.AUTH_REGISTER`:

```python
AUTH_REGISTER = {
    "email": "dev@exemplo.com",
    "password": "Senha@123",
    "confirm_password": "Senha@123",
    "name": "Ada Lovelace",
    "role": "Dev",
}
```

Em modo mock o wizard abre no step 2 (Confirmar) com avatar "AL", nome "Ada Lovelace", papel "Dev" e e-mail mock.
