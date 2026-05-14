# OnboardingWalkthroughWizard

Walkthrough mobile fullscreen em **4 slides + tela de sucesso**, com dots de progresso, botão "Pular" e CTA pill.

- **ID:** `onboarding.walkthrough`
- **Categoria:** `onboarding`
- **Módulo:** `flet_wizards.onboarding.walkthrough`
- **Importação pública:** `from flet_wizards import OnboardingWalkthroughWizard`

---

## Descrição

Tour de boas-vindas em 4 slides fullscreen, cada um com ícone grande em badge circular, título, subtítulo e CTA no bottom. Sem campos de entrada — onboarding é informativo. O usuário pode pular para o último slide a qualquer momento via botão "Pular" no topo direito.

`on_complete` recebe `{}` — não há dados a coletar, apenas a sinalização de que o usuário concluiu o tour.

---

## Quando usar

- Boas-vindas após primeira instalação do app.
- Apresentação de novas funcionalidades após major update.
- Tour rápido de features principais antes do uso.

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **Bem-vindo** | ✨ "Bem-vindo ao DayFlow" — apresentação do produto. |
| 1 | **Organize** | 📋 "Organize seu dia" — features de listas. |
| 2 | **Acompanhe** | 📈 "Acompanhe seu progresso" — features de métricas. |
| 3 | **Comece** | 🚀 "Pronto para começar?" — CTA final, botão muda para "Começar". |
| 4 | **Sucesso** | Check grande, "Tudo pronto!" e botão "Refazer tour". |

Os textos e ícones dos slides são definidos em `SLIDES: list[_Slide]` em `walkthrough.py`. Para customizar, fork o módulo (extensibilidade declarativa de slides está prevista para 0.3.0).

---

## Campos coletados

Nenhum. O wizard não tem state de formulário — apenas navegação.

---

## Parâmetros

| Parâmetro | Tipo | Default | Descrição |
|---|---|---|---|
| `theme` | `WizardTheme` | `WizardTheme.SLATE` | Paleta visual. |
| `on_complete` | `Callable[[dict], Any] \| None` | `None` | Callback recebendo `{}` ao clicar em "Começar". |
| `mock` | `bool` | `False` | Preview no gallery — abre direto no slide 3 (CTA "Começar"). |

---

## Plataformas suportadas

```python
[ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
```

Em desktop, o `PlatformGuard` exibe modal com botão "Continuar mesmo assim".

---

## Retorno do `on_complete`

```python
{}
```

Schema declarado em `META.on_complete_schema = {}`. O dict vazio é intencional — o wizard apenas sinaliza conclusão.

---

## Limitações conhecidas

- **Slides hardcoded.** Os 4 slides (textos, ícones, ordem) estão definidos no módulo. Para customizar, é preciso forkar — a parametrização de slides via prop está prevista para 0.3.0.
- **Sem `on_skip` hook.** Clicar em "Pular" apenas pula para o último slide internamente; o app consumidor não é notificado.
- **Sem `on_slide_change` hook.** Não há como o consumidor reagir a transições entre slides (ex: analytics de qual slide o usuário viu).

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import OnboardingWalkthroughWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_done(_: dict) -> None:
        # marcar onboarding como concluído no storage local
        ...

    return OnboardingWalkthroughWizard(
        theme=WizardTheme.EMERALD,
        on_complete=handle_done,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.render(App)


ft.run(main)
```

---

## Mock no gallery

Não há entrada em `mock_data` para este wizard — o conteúdo dos slides é estático em `SLIDES`. Em modo mock, o state apenas avança para o slide 3 (`step = TOTAL_STEPS - 1`) onde o CTA "Começar" está visível.
