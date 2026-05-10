# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o versionamento usa [SemVer](https://semver.org/lang/pt-BR/).

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
