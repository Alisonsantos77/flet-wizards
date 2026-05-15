# Contributing to flet-wizards

🌐 [Português](CONTRIBUTING.pt-BR.md) | **English**

> To use the library, see the [README](README.md). This file is for anyone contributing new templates or improvements.

---

## Local setup

```powershell
git clone https://github.com/Alisonsantos77/flet-wizards
cd flet-wizards
uv sync
uv run flet run
```

`uv run flet run` boots the local preview with every wizard. To inspect a wizard in isolation:

```bash
uv run python preview/run.py
```

---

## Project layout

```
flet-wizards/
├── src/
│   ├── flet_wizards/        ← package published to PyPI
│   │   ├── __init__.py      ← public API (re-exports) + __version__
│   │   ├── auth/            ← login, register, recovery, two_factor
│   │   ├── profile/         ← setup, edit, avatar
│   │   ├── onboarding/      ← walkthrough (mobile)
│   │   ├── survey/          ← feedback (mobile)
│   │   └── core/            ← state, frame, components, theme, registry, snack
│   ├── gallery/             ← dev preview, not shipped in the wheel
│   └── main.py              ← flet run entrypoint, not shipped in the wheel
├── docs/                    ← per-wizard documentation (written by hand)
├── preview/                 ← alternative preview script, not in the wheel
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
└── CONTRIBUTING.md          ← this file
```

Only `src/flet_wizards/` is included in the wheel published to PyPI. `src/gallery/`, `src/main.py`, `preview/`, `docs/` and `testers/` are excluded.

---

## Adding a new template

### 1. Create the module

`src/flet_wizards/<category>/<name>.py`. Existing categories: `auth`, `profile`, `onboarding`, `survey`. New categories can be added freely.

### 2. Declare `WizardMeta` at the top

```python
import flet as ft
from flet_wizards.core import WizardMeta, register

META = register(
    WizardMeta(
        id="category.name",
        name="Template Name",
        category="category",
        description="Short description.",
        steps=["Step 1", "Step 2"],
        platforms=[
            ft.PagePlatform.WINDOWS,
            ft.PagePlatform.MACOS,
            ft.PagePlatform.LINUX,
            ft.PagePlatform.ANDROID,
            ft.PagePlatform.IOS,
        ],
        on_complete_schema={"field": "str"},
    )
)
```

### 3. Define the reactive state

```python
from dataclasses import dataclass
from typing import ClassVar
import flet as ft
from flet_wizards.core import BaseWizardState


@ft.observable
@dataclass
class MyState(BaseWizardState):
    TOTAL_STEPS: ClassVar[int] = 2
    field: str = ""

    def reset(self) -> None:
        super().reset()
        self.field = ""
```

### 4. Build step components at module scope

`@ft.component` must never be nested inside another function — hook registration breaks and the UI silently freezes.

```python
@ft.component
def StepA(state: MyState) -> ft.Control:
    ...
```

### 5. Build the public wizard

Use `WizardFrame` for desktop+mobile wizards with a sidebar. For mobile-first wizards (Android/iOS only), build the frame manually without a sidebar.

```python
@ft.component
def MyWizard(
    theme: WizardTheme = WizardTheme.SLATE,
    on_complete: Callable[[dict], Any] | None = None,
    mock: bool = False,
) -> ft.Control:
    state, _ = ft.use_state(MyState(theme=theme))
    return WizardFrame(
        state=state,
        step_labels=["A", "B"],
        step_hints=["...", "..."],
        steps=[StepA, StepB, StepSuccess],
        on_complete=on_complete,
    )
```

### 6. Add mock data

`src/flet_wizards/core/mock_data.py`:

```python
MY_TEMPLATE: dict = {"field": "sample value"}
```

### 7. Re-export from `src/flet_wizards/__init__.py`

```python
from flet_wizards.<category>.<name> import MyWizard

__all__ = [..., "MyWizard"]
```

### 8. Register in the gallery

Import the module from `src/gallery/app.py`. `register()` is idempotent and the card is rendered from the registry.

### 9. Document

Create `docs/<category>/<name>.md` following the standard structure (description, steps, fields per step, platforms, `on_complete` return value, usage example, mock data).

### 10. Update the CHANGELOG

Add an entry under the next `[X.Y.Z]` section of `CHANGELOG.md`, following Keep a Changelog.

---

## Coding conventions

### Forbidden
- `page.update()` under any circumstance — Flet 0.85+ has auto-update.
- `print()` — use `loguru.logger`.
- Inline comments — only technical docstrings.
- Hardcoded hex colors outside `WizardTheme` (exceptions: `#EF4444` error, `#22C55E` success, `#F59E0B` warning).
- `@ft.component` nested inside another function.

### User feedback

Always via helpers from `flet_wizards.core.snack`:

```python
from flet_wizards.core import show_success, show_error, show_info
```

`SnackHost` is mounted once at the top of the app (the README example does this implicitly; apps that need snacks outside wizards should mount it explicitly).

### Animations

```python
ft.Animation(300, ft.AnimationCurve.EASE_OUT_CUBIC)  # general default
# AnimatedSwitcher: duration=260, FADE, key=str(state.step) — required
```

### Flet APIs — inspect before using

```bash
uv run python -c "import inspect, flet as ft; print(inspect.signature(ft.ClassName))"
```

Pitfalls already mapped:
- `ft.Dropdown` → `on_select` (not `on_change`)
- `ft.Image` → `ft.BoxFit` (not `ft.ImageFit` — does not exist)
- `ft.PagePlatform` → has no `.WEB` (use `page.web`)
- `ft.use_dialog(control)` → accepts a control or None, does not return a tuple
- `page.push_route()` → is a coroutine, requires `await`

### Hybrid state pattern

Every form field combines local `use_state` with the global state:

```python
field_v, set_field = ft.use_state(state.field)

def on_change(e):
    set_field(e.control.value)      # immediate reactivity in the TextField
    state.field = e.control.value    # persistence across steps
```

Without the local `use_state`, the field does not react while the user types.
Without `state.field =`, the value is lost when navigating between steps.

### Mobile-first — differences

When `platforms=[ANDROID, IOS]`:
1. Do not use `WizardFrame` — it ships with a desktop sidebar.
2. Build your own frame: header with dots, centered content, button at the bottom.
3. Minimum 48px height on clickable elements.
4. Correct `keyboard_type` on every `TextField` (`NUMBER`, `EMAIL`).

---

## Releases

Releases follow [SemVer](https://semver.org/):
- **Patch** (0.0.X): bug fix without breaking the API.
- **Minor** (0.X.0): new feature without breaking the API.
- **Major** (X.0.0): API break.

Flow:

```bash
# bump pyproject.toml and src/flet_wizards/__init__.py
# update CHANGELOG.md
uv sync
git add pyproject.toml src/flet_wizards/__init__.py CHANGELOG.md uv.lock
git commit -m "chore: bump version to X.Y.Z"
git push
git tag vX.Y.Z
git push origin vX.Y.Z
```

The `publish.yml` workflow handles the PyPI upload via Trusted Publisher OIDC.

---

## Reporting bugs

[github.com/Alisonsantos77/flet-wizards/issues](https://github.com/Alisonsantos77/flet-wizards/issues)
