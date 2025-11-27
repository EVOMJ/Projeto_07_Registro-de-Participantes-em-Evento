import json
import re
import os

ARQUIVO = "participantes.json"

# ------------------------------
#  Classe Participante
# ------------------------------
class Participante:
    def __init__(self, nome, email, cpf):
        self.nome = nome
        self.email = email
        self.cpf = cpf

    def to_dict(self):
        return {"nome": self.nome, "email": self.email, "cpf": self.cpf}


# ------------------------------
#   Funções Auxiliares
# ------------------------------

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    return len(cpf) == 11 and cpf.isdigit()

def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return []

def salvar_dados(participantes):
    with open(ARQUIVO, "w") as f:
        json.dump(participantes, f, indent=4)

def cpf_existe(participantes, cpf):
    return any(p["cpf"] == cpf for p in participantes)


# ------------------------------
#   Funções do Sistema
# ------------------------------

def cadastrar_participante(participantes):
    print("\n--- Cadastro de Participante ---")

    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip()
    cpf = input("CPF (somente números): ").strip()

    # Validações
    if not validar_email(email):
        print("❌ E-mail inválido!")
        return

    if not validar_cpf(cpf):
        print("❌ CPF inválido!")
        return

    if cpf_existe(participantes, cpf):
        print("❌ Já existe um participante com esse CPF!")
        return

    novo = Participante(nome, email, cpf)
    participantes.append(novo.to_dict())

    salvar_dados(participantes)
    print("✔ Participante cadastrado com sucesso!")

def listar_participantes(participantes):
    print("\n--- Lista de Participantes ---")
    if not participantes:
        print("Nenhum participante cadastrado.")
        return

    for i, p in enumerate(participantes, start=1):
        print(f"\nParticipante {i}:")
        print(f"  Nome:  {p['nome']}")
        print(f"  E-mail:{p['email']}")
        print(f"  CPF:   {p['cpf']}")

def buscar_participante(participantes):
    print("\n--- Buscar Participante ---")
    termo = input("Digite nome, parte do nome, e-mail ou CPF: ").lower()

    resultados = [
        p for p in participantes
        if termo in p["nome"].lower()
        or termo in p["email"].lower()
        or termo in p["cpf"]
    ]

    if not resultados:
        print("❌ Nenhum participante encontrado.")
        return

    print("\n✔ Resultados:")
    for p in resultados:
        print(f"\nNome: {p['nome']}")
        print(f"E-mail: {p['email']}")
        print(f"CPF: {p['cpf']}")

def remover_participante(participantes):
    print("\n--- Remover Participante ---")
    cpf = input("Digite o CPF: ")

    for p in participantes:
        if p["cpf"] == cpf:
            participantes.remove(p)
            salvar_dados(participantes)
            print("✔ Participante removido!")
            return

    print("❌ CPF não encontrado.")


# ------------------------------
#         Menu Principal
# ------------------------------

def menu():
    participantes = carregar_dados()

    while True:
        print("\n===== MENU =====")
        print("1 - Cadastrar participante")
        print("2 - Listar participantes")
        print("3 - Buscar participante")
        print("4 - Remover participante")
        print("5 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_participante(participantes)
        elif opcao == "2":
            listar_participantes(participantes)
        elif opcao == "3":
            buscar_participante(participantes)
        elif opcao == "4":
            remover_participante(participantes)
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

menu()
