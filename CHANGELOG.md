# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o versionamento usa [SemVer](https://semver.org/lang/pt-BR/).

## [0.2.3] — 2026-05-14

Release de documentação. Sem mudanças funcionais — alinha README, `docs/` e guia de contribuição ao estado real entregue em 0.2.2.

### Adicionado

- **`LICENSE`** na raiz do repositório (MIT, 2026, Alison Santos). Incluído em `[tool.hatch.build.targets.sdist].include` — sdist publicado no PyPI agora carrega a licença.
- **`CONTRIBUTING.md`** separado do README. Concentra setup local, estrutura do projeto, passo a passo de 10 itens para adicionar template novo, convenções de código, padrão híbrido de estado, diferenças mobile-first e fluxo de release.
- **`docs/themes.md`** — documentação pública do sistema de tema duplo dark/light: tabela dos 7 pares, tokens de cor, uso direto (`WizardTheme.X` / `WizardTheme.X_LIGHT`), `resolve_theme(theme, mode)` com fallbacks, convenções de bg em temas saturados, paletas customizadas.
- **`docs/auth/two_factor.md`**, **`docs/onboarding/walkthrough.md`**, **`docs/survey/feedback.md`** — docs completas dos 3 wizards mobile-first introduzidos em 0.2.0 (descrição, quando usar, steps, campos, parâmetros, plataformas, limitações conhecidas, exemplo, mock data).

### Alterado

- **`README.md`** reescrito para refletir 0.2.x: tabela com os 9 wizards atuais (incluindo `AuthTwoFactorWizard`, `OnboardingWalkthroughWizard`, `SurveyFeedbackWizard`), seção dedicada a Temas com tabela dos 7 pares e exemplo de `resolve_theme`, seção "Preview local de desenvolvimento" explicitando que `src/gallery/` não vai no wheel, seção "Demo interativa" linkando o repo separado de showcase. Seção "Contribuindo" reduzida a uma linha apontando para `CONTRIBUTING.md`. Badge MIT passa a apontar para `./LICENSE`.
- **`docs/profile/avatar.md`** reescrito — remove toda menção a "Arquivo"/`_PanelArquivo`/`state.file_path` (origem removida em 0.2.1). Documenta 2 origens (URL e Iniciais), corrige mock data (`bg_color=""` com fallback em `state.accent()`), adiciona seção de limitações conhecidas.
- **`docs/profile/setup.md`** — tabela do step Preferências atualizada para refletir os 4 swatches reais (`Slate`, `Rose`, `Amber`, `Frost`). Nota explicando que os demais temas (`Emerald`, `Azure`, `Crimson`) continuam acessíveis via `WizardTheme.X` direto.

## [0.2.2] — 2026-05-14

Release focado em sistema de tema duplo dark/light, retrabalho de paletas e melhorias de legibilidade de UI.

### Adicionado

- **Sistema de tema duplo dark/light** — `WizardTheme` ganhou os campos `mode: ft.ThemeMode` e `pair_name: str`. Cada combinação existe em 2 variantes (14 paletas no total): `SLATE`/`SLATE_LIGHT`, `EMERALD`/`EMERALD_LIGHT`, `ROSE`/`ROSE_LIGHT`, `AZURE`/`AZURE_LIGHT`, `AMBER`/`AMBER_LIGHT`, `CRIMSON`/`CRIMSON_LIGHT`, `FROST_DARK`/`FROST`. Dict `THEME_PAIRS` mapeia `pair_name → (dark, light)`.
- **`resolve_theme(theme, mode)`** — função pública em `flet_wizards.core` que devolve a variante correta para um `ft.ThemeMode`. Em `SYSTEM`, lê `ft.context.page.platform_brightness` e cai em dark como fallback fora de contexto reativo.
- **Toggle de ThemeMode no preview** — barra com 3 estados (SYSTEM / LIGHT / DARK) abaixo do seletor de temas. Filtra os swatches por modo e converte automaticamente o tema ativo para a variante oposta do mesmo par ao trocar de modo.

### Alterado

- **Rename `WizardTheme.FOREST` → `WizardTheme.AMBER`** (`FOREST_LIGHT` → `AMBER_LIGHT`, `pair_name` `"forest"` → `"amber"`). O nome reflete melhor a identidade da cor (`#F59E0B`).
- **Paletas reworked** — `EMERALD`, `ROSE`, `AZURE` e `AMBER` ganharam tokens novos com melhor balanço entre `primary`, `accent` e `panel`. `SLATE` e `CRIMSON` mantêm a identidade mas com ajustes finos.
- **Bg neutro escuro em temas dark de alta saturação** — `ROSE` e `AMBER` dark passam a usar `bg`/`surface`/`card` neutros (`#0D0D0D`/`#161616`/`#1C1C1C`) para que a identidade da cor fique no `primary`/`accent` sem contaminar o fundo. Identidades visualmente distintas mesmo entre temas com a mesma família de bg.
- **Light themes com fundo branco neutro** — todas as 7 variantes light agora têm `bg=#FFFFFF`, `surface=#FFFFFF`, `card=#FAFAFA`. Tint da cor identidade é preservado apenas em `panel` (sidebar). Border padronizado em `#E2E8F0` neutro.
- **`primary_button` sempre com texto branco** — heurística por luminância removida. `text_color` explícito ainda sobrescreve. A heurística produzia regressões em ambos os extremos do espectro (Amber dark `#F59E0B` ganhava texto escuro, Amber light `#D97706` também). Branco em todos os botões CTA segue a convenção de libs maduras.
- **Sidebar dos wizards desktop — legibilidade independente do tema** — label e hint do step ativo agora usam `state.text()`; demais steps (inativo ou completado) usam `state.sub()`. `state.primary()` permanece apenas em bgcolor do círculo do step ativo, indicator vertical e barra de progresso. Garante leitura mesmo em temas com primary muito saturado (Amber, Rose).
- **`ProfileSetupWizard` step Preferências** — seletor de tema enxuto com 4 swatches (Slate, Rose, Amber, Frost) em vez de exibir todos os 7 do registro.
- **`AuthRegisterWizard` step Confirmar** — badge do role substituído por texto inline `"Nome (Role)"` em `ft.Text` simples. Sem container bordado.
- **`ProfileAvatarWizard`** — `bg_color` do mock vazio por default; círculo do avatar herda `state.accent()` quando o usuário ainda não escolheu cor.

### Documentação

- Docstrings de `core/theme.py` atualizadas para descrever pares dark/light, convenção de bg neutro e fallback de `resolve_theme` em SYSTEM.

## [0.2.1] — 2026-05-13

Release de bugfixes focado em contraste, foco assíncrono nos campos de OTP e ajustes da paleta âmbar.

### Corrigido

- **`AuthTwoFactorWizard`** — guarda `try/except` em torno do `field.focus()` (chamada assíncrona pode lançar `AssertionError` se o controle ainda não estiver no tree); `on_submit` agora avança o foco para o próximo dígito após digitação. Auto-advance via `on_change` foi removido temporariamente até revisão.
- **`primary_button`** — contraste de texto recalculado sobre `theme.primary` para garantir leitura em todos os modos (resolveu botões "invisíveis" na paleta âmbar).
- **Paleta `WizardTheme.AMBER`** — `primary` retrabalhado para tom âmbar saturado com contraste adequado contra `bg` e `surface`; `accent` e `panel` rebalanceados.
- **`ProfileAvatarWizard`** — cor do mock do avatar agora deriva de `theme.surface` em vez de hex fixo.
- **Seletor de tema** — ring do tema ativo agora respeita `theme.primary` corrente.
- **`badge`** em mock data — cores derivadas do tema (não mais hex hardcoded).
- **`preview/run.py`** — layout sem `Container` constrangedor (preview redimensionável); imports diretos a partir de `src/flet_wizards/`.

## [0.2.0] — 2026-05-12

Release focado em ampliar o catálogo com 3 wizards mobile-first e melhorar a sinalização de wizards rodando em modo demo.

### Adicionado

- **`AuthTwoFactorWizard`** (`flet_wizards.AuthTwoFactorWizard`) — verificação em 2 fatores mobile-first com 6 campos individuais de dígito, fundo geométrico via `ft.Stack` (sem imagem externa) e validação local exigindo os 6 dígitos antes de confirmar. Plataformas: ANDROID, IOS. `on_complete` recebe `{"code": str}`.
- **`OnboardingWalkthroughWizard`** (`flet_wizards.OnboardingWalkthroughWizard`) — walkthrough fullscreen em 4 slides com cabeçalho "Pular", ícone grande em badge circular, dots de progresso e CTA pill ("Próximo →" / "Começar"). Plataformas: ANDROID, IOS. `on_complete` recebe `{}` (apenas sinaliza conclusão).
- **`SurveyFeedbackWizard`** (`flet_wizards.SurveyFeedbackWizard`) — survey conversacional estilo Typeform em 3 perguntas: NPS 0-10 colorido por faixa, comentário livre com contador de caracteres (`COMMENT_LIMIT=280`) e categoria (Bug / Sugestão / Elogio) em cards grandes. Plataformas: ANDROID, IOS. `on_complete` recebe `{"nps": int, "comment": str, "category": str}`.
- **Novos módulos públicos** `flet_wizards.onboarding` e `flet_wizards.survey`, exportando os wizards correspondentes a partir do package raiz.
- **Mock data** para os 3 novos templates em `flet_wizards.core.mock_data`: `AUTH_TWO_FACTOR`, `SURVEY_FEEDBACK` (`OnboardingWalkthroughWizard` não precisa de mock data — apenas reposiciona `step`).

### Alterado

- **`on_complete=None` agora emite `logger.warning`** em todos os 9 wizards antes do early return silencioso, deixando claro nos logs que o template está rodando em modo demo. Mensagem padronizada: `"[NomeDoWizard]: on_complete não fornecido — wizard funcionará como demo"`.
- **`preview/run.py`** revisado para subir limpo localmente — todos os 9 wizards podem ser inspecionados via `uv run python preview/run.py`.

## [0.1.1] — 2026-05-10

Release de housekeeping focado em metadados PyPI e documentação. Sem mudanças funcionais nos wizards — a API pública é idêntica à 0.1.0.

### Removido

- Pipeline `pipeline/cocoindex_pipeline.py` e `pipeline/__init__.py` que geravam docs via OpenAI.
- Workflow `.github/workflows/docs.yml` que disparava o pipeline a cada push.
- Dependência opcional `openai` (extra `[pipeline]`) do `pyproject.toml`.

### Alterado

- **Documentação dos templates** (`docs/`) agora é escrita pelo Claude Code lendo o código fonte sob demanda e commitada manualmente. Não há mais geração automática nem chamadas a APIs externas.
- **Metadados PyPI** atualizados em `pyproject.toml`:
  - `keywords = ["flet", "wizard", "ui", "components", "python", "mobile", "desktop"]`.
  - Classifiers movidos para `Development Status :: 4 - Beta`, com `Topic :: Software Development :: Widget Sets`, `Operating System :: OS Independent` e `Typing :: Typed` adicionados.
  - `[project.urls]` ampliado com `Repository`, `Issues` e `Changelog`.
- **README.md** reescrito com badge de versão PyPI, tabela de templates linkando docs, instruções reais de instalação (`pip install flet-wizards`), exemplo de uso atualizado e seção "Contribuindo" detalhando o passo a passo de adicionar um novo template via `WizardMeta`.

## [0.1.0] — 2026-05-10

Primeiro release público no PyPI. Foco em validar a API pública dos wizards e o gallery showcase antes de iniciar a fase de extensão (v0.2.0).

### Adicionado

- **6 wizards prontos para uso**, todos como `@ft.component` autocontidos com state `@ft.observable`:
  - `AuthLoginWizard` — login clássico (e-mail + senha) em 2 steps + sucesso.
  - `AuthRegisterWizard` — cadastro (conta + perfil + revisão) em 3 steps + sucesso.
  - `AuthRecoveryWizard` — recuperação de senha com código de 6 dígitos e indicador de força animado em 3 steps + sucesso.
  - `ProfileSetupWizard` — onboarding com identidade, bio, interesses e preferências (tema ao vivo) em 3 steps + sucesso.
  - `ProfileEditWizard` — edição com diff visual de campos alterados em 3 steps + sucesso.
  - `ProfileAvatarWizard` — configuração de avatar via arquivo, URL ou iniciais em 3 steps + sucesso.
- **Gallery showcase** estilo Microsoft Store em `src/gallery/`, usando `ft.Router` com `manage_views=False`, sidebar por categoria, header com seletor de tema e área principal trocada via `AnimatedSwitcher`.
- **Sistema de temas** com 4 paletas built-in (Slate, Emerald, Rose, Azure) expostas como `WizardTheme.SLATE`, `WizardTheme.EMERALD`, `WizardTheme.ROSE`, `WizardTheme.AZURE`. Paleta customizável via `WizardTheme(...)`.
- **Mock data** centralizado em `flet_wizards.core.mock_data` para preview no gallery — cada wizard aceita `mock: bool = False` que inicializa o state com dados de exemplo e abre direto no último step de dados.
- **Platform guard** via `ft.PagePlatform`, com tela de "Template não compatível" e botão de bypass usando `ft.use_dialog()`.
- **SnackHost** centralizado com `show_success` / `show_error` / `show_info`, montado uma única vez no topo do app via `ft.use_dialog()`.
- **WizardMeta** declarativo no topo de cada template, alimentando o gallery e a documentação.
- **Distribuição PyPI** via `hatchling` + Trusted Publisher (OIDC), com `gallery/`, `src/main.py`, `src/assets/`, `docs/`, `storage/` e `.github/` excluídos do wheel.

### Notas

- Suporta Python 3.12+ e Flet 0.85+.
- Todos os wizards atuais funcionam em Windows, macOS, Linux, Android, iOS e Web. Em web, `ft.PagePlatform` não inclui `WEB`; usar `page.web` (boolean) para detecção.
