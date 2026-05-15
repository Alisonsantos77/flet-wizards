# Contribuindo com flet-wizards

🌐 **Português** | [English](CONTRIBUTING.md)

> Para usar a lib, veja o [README](README.pt-BR.md). Este arquivo é para quem quer contribuir com novos templates ou melhorias.

---

## Setup local

```powershell
git clone https://github.com/Alisonsantos77/flet-wizards
cd flet-wizards
uv sync
uv run flet run
```

`uv run flet run` sobe o preview local com todos os wizards. Para inspecionar um wizard isolado:

```bash
uv run python preview/run.py
```

---

## Estrutura do projeto

```
flet-wizards/
├── src/
│   ├── flet_wizards/        ← pacote publicado no PyPI
│   │   ├── __init__.py      ← API pública (re-exports) + __version__
│   │   ├── auth/            ← login, register, recovery, two_factor
│   │   ├── profile/         ← setup, edit, avatar
│   │   ├── onboarding/      ← walkthrough (mobile)
│   │   ├── survey/          ← feedback (mobile)
│   │   └── core/            ← state, frame, components, theme, registry, snack
│   ├── gallery/             ← preview de dev, fora do wheel
│   └── main.py              ← entrypoint do flet run, fora do wheel
├── docs/                    ← documentação por wizard (escrita manualmente)
├── preview/                 ← script alternativo de preview, fora do wheel
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
└── CONTRIBUTING.md          ← este arquivo
```

Apenas `src/flet_wizards/` vai no wheel publicado no PyPI. `src/gallery/`, `src/main.py`, `preview/`, `docs/` e `testers/` ficam fora.

---

## Adicionar um novo template

### 1. Criar o módulo

`src/flet_wizards/<categoria>/<nome>.py`. Categorias existentes: `auth`, `profile`, `onboarding`, `survey`. Categorias novas podem ser criadas livremente.

### 2. Declarar o `WizardMeta` no topo

```python
import flet as ft
from flet_wizards.core import WizardMeta, register

META = register(
    WizardMeta(
        id="categoria.nome",
        name="Nome do Template",
        category="categoria",
        description="Descrição curta.",
        steps=["Step 1", "Step 2"],
        platforms=[
            ft.PagePlatform.WINDOWS,
            ft.PagePlatform.MACOS,
            ft.PagePlatform.LINUX,
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
        ],
        on_complete_schema={"campo": "str"},
    )
)
```

### 3. Definir o state reativo

```python
from dataclasses import dataclass
from typing import ClassVar
import flet as ft
from flet_wizards.core import BaseWizardState


@ft.observable
@dataclass
class MeuState(BaseWizardState):
    TOTAL_STEPS: ClassVar[int] = 2
    campo: str = ""

    def reset(self) -> None:
        super().reset()
        self.campo = ""
```

### 4. Criar os step components em escopo de módulo

`@ft.component` nunca aninhado dentro de outra função — o registro de hooks quebra e a UI congela silenciosamente.

```python
@ft.component
def StepA(state: MeuState) -> ft.Control:
    ...
```

### 5. Construir o wizard público

Use `WizardFrame` para wizards desktop+mobile com sidebar. Para mobile-first (Android/iOS apenas), construa o frame manualmente sem sidebar.

```python
@ft.component
def MeuWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: Callable[[dict], Any] | None = None,
    mock: bool = False,
) -> ft.Control:
    state, _ = ft.use_state(MeuState(theme=theme))
    return WizardFrame(
        state=state,
        step_labels=["A", "B"],
        step_hints=["...", "..."],
        steps=[StepA, StepB, StepSuccess],
        on_complete=on_complete,
    )
```

### 6. Adicionar mock data

`src/flet_wizards/core/mock_data.py`:

```python
MEU_TEMPLATE: dict = {"campo": "valor de exemplo"}
```

### 7. Re-exportar no `src/flet_wizards/__init__.py`

```python
from flet_wizards.<categoria>.<nome> import MeuWizard

__all__ = [..., "MeuWizard"]
```

### 8. Registrar no gallery

Importar o módulo em `src/gallery/app.py`. O `register()` é idempotente e o card é renderizado a partir do registry.

### 9. Documentar

Criar `docs/<categoria>/<nome>.md` seguindo a estrutura padrão (descrição, steps, campos por step, plataformas, retorno de `on_complete`, exemplo de uso, mock data).

### 10. Atualizar o CHANGELOG

Adicionar entrada na próxima seção `[X.Y.Z]` do `CHANGELOG.md` seguindo Keep a Changelog.

---

## Convenções de código

### Proibido
- `page.update()` em qualquer circunstância — Flet 0.85+ tem auto-update.
- `print()` — use `loguru.logger`.
- Comentários inline — apenas docstrings técnicas.
- Hex hardcoded fora do `WizardTheme` (exceto `#EF4444` erro, `#22C55E` sucesso, `#F59E0B` aviso).
- `@ft.component` aninhado dentro de outra função.

### Feedback ao usuário

Sempre via helpers do `flet_wizards.core.snack`:

```python
from flet_wizards.core import show_success, show_error, show_info
```

O `SnackHost` é montado uma vez no topo do app (no exemplo do README isso já vem implícito; em apps que precisam de snacks fora dos wizards, monte explicitamente).

### Animações

```python
ft.Animation(300, ft.AnimationCurve.EASE_OUT_CUBIC)  # padrão geral
# AnimatedSwitcher: duration=260, FADE, key=str(state.step) — obrigatório
```

### APIs Flet — inspecionar antes de usar

```bash
uv run python -c "import inspect, flet as ft; print(inspect.signature(ft.NomeDaClasse))"
```

Armadilhas já mapeadas:
- `ft.Dropdown` → `on_select` (não `on_change`)
- `ft.Image` → `ft.BoxFit` (não `ft.ImageFit` — não existe)
- `ft.PagePlatform` → sem `.WEB` (usar `page.web`)
- `ft.use_dialog(control)` → recebe control ou None, não retorna tupla
- `page.push_route()` → é coroutine, precisa de `await`

### Padrão híbrido de estado

Cada campo de formulário combina `use_state` local com estado global:

```python
campo_v, set_campo = ft.use_state(state.campo)

def on_change(e):
    set_campo(e.control.value)      # reatividade imediata no TextField
    state.campo = e.control.value    # persistência entre steps
```

Sem o `use_state` local, o campo não reage enquanto o usuário digita.
Sem o `state.campo =`, o valor se perde ao navegar entre steps.

### Mobile-first — diferenças

Se `platforms=[ANDROID, IOS]`:
1. Não usar `WizardFrame` — ele tem sidebar desktop.
2. Construir frame próprio: header com dots, conteúdo centralizado, botão no bottom.
3. Altura mínima de 48px em elementos clicáveis.
4. `keyboard_type` correto em cada `TextField` (`NUMBER`, `EMAIL`).

---

## Releases

Releases seguem [SemVer](https://semver.org/):
- **Patch** (0.0.X): bug fix sem quebrar API.
- **Minor** (0.X.0): feature nova sem quebrar API.
- **Major** (X.0.0): quebra de API.

Fluxo:

```bash
# bumpar pyproject.toml e src/flet_wizards/__init__.py
# atualizar CHANGELOG.md
uv sync
git add pyproject.toml src/flet_wizards/__init__.py CHANGELOG.md uv.lock
git commit -m "chore: bump version to X.Y.Z"
git push
git tag vX.Y.Z
git push origin vX.Y.Z
```

O workflow `publish.yml` cuida do upload no PyPI via Trusted Publisher OIDC.

---

## Reportar bugs

[github.com/Alisonsantos77/flet-wizards/issues](https://github.com/Alisonsantos77/flet-wizards/issues)
