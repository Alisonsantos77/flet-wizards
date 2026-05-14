"""Dados mock para preenchimento automático no modo demonstrativo.

Cada wizard expõe um parâmetro `mock: bool = False`. Quando `True`, o state
é inicializado com o dict correspondente desta lista. O gallery sempre passa
`mock=True`; quem importar a biblioteca futuramente usa `mock=False`.

Convenção complementar: no modo mock o wizard abre no último step de dados
(`TOTAL_STEPS - 1`), funcionando como preview rápido. O dev navega para o
início clicando em "Voltar".

Os valores aqui são fictícios e seguros para screenshots/GIFs públicos.
"""

AUTH_LOGIN: dict = {
    "email": "dev@exemplo.com",
    "password": "Senha@123",
}

AUTH_REGISTER: dict = {
    "email": "dev@exemplo.com",
    "password": "Senha@123",
    "confirm_password": "Senha@123",
    "name": "Ada Lovelace",
    "role": "Dev",
}

AUTH_RECOVERY: dict = {
    "email": "dev@exemplo.com",
    "code": "429731",
    "new_password": "NovaSenha@123",
    "confirm_password": "NovaSenha@123",
}

PROFILE_SETUP: dict = {
    "name": "Ada Lovelace",
    "username": "ada.lovelace",
    "bio": "Engenheira de software apaixonada por sistemas distribuídos.",
    "interests": ["Python", "DevOps"],
    "theme_key": "Slate",
    "language": "pt-BR",
}

PROFILE_EDIT: dict = {
    "name": "Ada Lovelace",
    "email": "dev@exemplo.com",
    "phone": "+55 11 91234-5678",
    "current_password": "",
    "new_password": "",
    "confirm": "",
}

PROFILE_AVATAR: dict = {
    "source": "Iniciais",
    "initials": "AL",
    "bg_color": "",
}

SURVEY_FEEDBACK: dict = {
    "nps": 9,
    "comment": "O fluxo de revisão de PRs ficou muito mais rápido depois da última atualização.",
    "category": "Elogio",
}

AUTH_TWO_FACTOR: dict = {
    "code": "318274",
}
