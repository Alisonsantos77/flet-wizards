# SurveyFeedbackWizard

Survey conversacional mobile-first em **3 perguntas + tela de sucesso**: NPS, comentário livre e categoria.

- **ID:** `survey.feedback`
- **Categoria:** `survey`
- **Módulo:** `flet_wizards.survey.feedback`
- **Importação pública:** `from flet_wizards import SurveyFeedbackWizard`

---

## Descrição

Questionário leve estilo Typeform: uma pergunta por tela, fonte grande, inputs com personalidade. Mobile-first, sem sidebar. NPS (0-10) com chips coloridos por faixa (detrator vermelho, passivo amarelo, promotor verde), comentário livre com contador de caracteres (limite 280) e categoria do feedback em 3 cards grandes.

Validação por step: NPS exige seleção, comentário aceita vazio, categoria exige seleção. Em falha, dispara `show_error` em vez de avançar.

---

## Quando usar

- Coleta de NPS pós-onboarding ou após uso de feature crítica.
- Feedback após release significativo.
- Pesquisas curtas dentro do app, sem precisar de form builder externo.

---

## Steps

| Índice | Label | Conteúdo |
|---|---|---|
| 0 | **Nota** | Chips numerados 0-10, coloridos por faixa NPS. |
| 1 | **Motivo** | TextField multiline com contador `{used}/280`. |
| 2 | **Categoria** | 3 cards grandes: 🐞 Bug, 💡 Sugestão, 💚 Elogio. |
| 3 | **Sucesso** | Check, "Obrigado pelo retorno!" e resumo curto (`Nota X · Categoria`). |

---

## Campos coletados

| Campo | Tipo | Descrição |
|---|---|---|
| `nps` | `int` | -1 (não escolhido) ou 0-10. |
| `comment` | `str` | Texto livre até 280 caracteres (limite enforced via slice no `on_change`). |
| `category` | `str` | `"Bug"`, `"Sugestão"` ou `"Elogio"`. |

Faixas NPS:

| Valor | Faixa | Cor |
|---|---|---|
| 0-6 | Detrator | `#EF4444` |
| 7-8 | Passivo | `#F59E0B` |
| 9-10 | Promotor | `#22C55E` |

---

## Parâmetros

| Parâmetro | Tipo | Default | Descrição |
|---|---|---|---|
| `theme` | `WizardTheme` | `WizardTheme.SLATE` | Paleta visual. |
| `on_complete` | `Callable[[dict], Any] \| None` | `None` | Callback recebendo `{"nps": int, "comment": str, "category": str}`. |
| `mock` | `bool` | `False` | Preview no gallery — abre no step 2 (Categoria) com `SURVEY_FEEDBACK`. |

---

## Plataformas suportadas

```python
[ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
```

Em desktop, o `PlatformGuard` exibe modal com botão "Continuar mesmo assim".

---

## Retorno do `on_complete`

```python
{"nps": int, "comment": str, "category": str}
```

Schema declarado em `META.on_complete_schema = {"nps": "int", "comment": "str", "category": "str"}`.

---

## Limitações conhecidas

- **Contexto fictício hardcoded.** O header diz "DevFlow · feedback" e a pergunta menciona "recomendar o DevFlow". Para usar em outro produto, fork o módulo — i18n e customização de textos está prevista para 0.3.0.
- **Categorias hardcoded.** As 3 opções (Bug, Sugestão, Elogio) estão definidas em `CATEGORIES` no módulo.
- **Sem `on_step_change` hook.** O app consumidor não é notificado entre transições (ex: salvar parcial após step 1).
- **Limite 280 chars hardcoded.** `COMMENT_LIMIT` é constante de módulo, não parametrizável.

---

## Exemplo de uso

```python
import flet as ft
from flet_wizards import SurveyFeedbackWizard, WizardTheme


@ft.component
def App() -> ft.Control:
    async def handle_feedback(data: dict) -> None:
        # data == {"nps": 9, "comment": "...", "category": "Elogio"}
        # POST /api/feedback ...
        ...

    return SurveyFeedbackWizard(
        theme=WizardTheme.AZURE,
        on_complete=handle_feedback,
    )


async def main(page: ft.Page) -> None:
    page.padding = 0
    page.render(App)


ft.run(main)
```

---

## Mock no gallery

`flet_wizards.core.mock_data.SURVEY_FEEDBACK`:

```python
SURVEY_FEEDBACK = {
    "nps": 9,
    "comment": "O fluxo de revisão de PRs ficou muito mais rápido depois da última atualização.",
    "category": "Elogio",
}
```

Em modo mock o wizard abre no step 2 (Categoria) com "Elogio" pré-selecionado.
