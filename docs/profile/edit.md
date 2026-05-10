# ProfileEditWizard

Edição de perfil em **3 steps de dados + tela de sucesso**, com diff visual destacando apenas campos alterados.

- **ID:** `profile.edit`
- **Categoria:** `profile`
- **Módulo:** `flet_wizards.profile.edit`
- **Importação pública:** `from flet_wizards import ProfileEditWizard`

---

## Descrição

Wizard reutilizável para telas de "Editar perfil". Recebe `initial_data: dict` com os valores atuais; pré-popula os campos no state e mantém o snapshot original para o diff. O step de confirmação mostra apenas os campos que mudaram, no formato `valor_antigo → valor_novo`.

`on_complete` recebe `{"changed_fields": dict}` — apenas o delta. Senhas são tratadas separadamente: se `new_password` foi preenchido, o diff inclui `("Senha", "•••", "atualizada")` e o payload contém `"password": "updated"` (nunca a senha em texto plano).

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **Dados** | Nome + e-mail + telefone (pré-populados). |
| 1 | **Segurança** | Senha atual + nova + confirmação (todos opcionais). |
| 2 | **Confirmar** | Diff visual: só os campos modificados, com `old → new`. |
| 3 | **Sucesso** | "Perfil atualizado." + botão "Voltar ao início". |

---

## Campos por step

### Step 0 — Dados

| Campo | Tipo | UI |
|---|---|---|
| `name` | `str` | `form_field("NOME", ..., "Nome completo")` |
| `email` | `str` | `form_field("E-MAIL", ..., "voce@exemplo.com")` |
| `phone` | `str` | `form_field("TELEFONE", ..., "+55 11 90000-0000")` |

### Step 1 — Segurança

| Campo | Tipo | UI |
|---|---|---|
| `current_password` | `str` | `form_field("SENHA ATUAL", ..., password=True, can_reveal_password=True)` |
| `new_password` | `str` | `form_field("NOVA SENHA", ..., password=True, can_reveal_password=True)` |
| `confirm` | `str` | `form_field("CONFIRMAR", ..., password=True, can_reveal_password=True)` |

Aviso "As senhas não coincidem." aparece se `confirm != new_password`. Tudo opcional — manter em branco preserva a senha atual.

### Step 2 — Confirmar

Renderização condicional via `_changed_fields(state)`:

- Se nada mudou: "Nada a alterar" + "Nenhum campo foi modificado em relação ao original."
- Caso contrário: lista de cards `(label, old, new)` com `→` no centro, valores antigos em itálico e cor `sub`, valores novos em peso 600 e cor `text`.

`VISIBLE_FIELDS` controla quais campos entram no diff:

```python
VISIBLE_FIELDS = [
    ("name", "Nome"),
    ("email", "E-mail"),
    ("phone", "Telefone"),
]
```

### Step 3 — Sucesso

Check (72px) + "Perfil atualizado." + "Suas alterações foram salvas com sucesso." + botão "Voltar ao início" → `state.reset()` (que repõe os valores de `initial_data`).

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
{"changed_fields": dict}
```

Onde `changed_fields` contém só as chaves modificadas. Exemplo:

```python
# Usuário só mudou o telefone:
{"changed_fields": {"phone": "+55 11 99999-8888"}}

# Usuário também atualizou a senha:
{"changed_fields": {"phone": "+55 11 99999-8888", "password": "updated"}}
```

Schema declarado em `META.on_complete_schema = {"changed_fields": "dict"}`.

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import ProfileEditWizard, WizardTheme


CURRENT_USER = {
    "name": "Ada Lovelace",
    "email": "ada@exemplo.com",
    "phone": "+55 11 91234-5678",
}


@ft.component
def App() -> ft.Control:
    async def handle_edit(data: dict) -> None:
        changed = data["changed_fields"]
        if not changed:
            return
        # PATCH /api/me com `changed`
        ...

    return ProfileEditWizard(
        theme=WizardTheme.AZURE,
        initial_data=CURRENT_USER,
        on_complete=handle_edit,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.bgcolor = "#0B0B0F"
    page.render(App)


ft.run(main)
```

---

## Mock no gallery

`flet_wizards.core.mock_data.PROFILE_EDIT`:

```python
PROFILE_EDIT = {
    "name": "Ada Lovelace",
    "email": "dev@exemplo.com",
    "phone": "+55 11 91234-5678",
    "current_password": "",
    "new_password": "",
    "confirm": "",
}
```

Em modo mock o wizard simula uma alteração: `initial_data` é uma cópia de `PROFILE_EDIT`, e o state usa o mesmo dict mas com `phone="+55 11 99999-8888"`. Abre no step 2 (Confirmar) já mostrando o diff de telefone como exemplo. O parâmetro `initial_data` é ignorado quando `mock=True`.
