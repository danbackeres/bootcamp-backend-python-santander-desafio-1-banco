from abc import ABC, abstractmethod
from datetime import datetime
import os

# Histórico de transações
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Interface de transação
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Depósito
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor <= 0:
            print("Valor inválido para depósito!")
            return False
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")
        print("Depósito realizado com sucesso!")
        return True

# Saque
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > conta.saldo:
            print("Saldo insuficiente para saque!")
            return False
        elif self.valor > conta.limite:
            print("Valor do saque excede o limite permitido!")
            return False
        elif conta.numero_saques >= conta.limite_saques:
            print("Limite de saques diários atingido!")
            return False
        elif self.valor <= 0:
            print("Valor inválido para saque!")
            return False
        conta.saldo -= self.valor
        conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")
        conta.numero_saques += 1
        print("Saque realizado com sucesso!")
        return True

# Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Pessoa Física
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# Conta
class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

# Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

usuarios = []
contas = []

def criar_usuario():
    cpf = input("CPF (11 dígitos): ").strip()
    if not cpf.isdigit() or len(cpf) != 11:
        print("CPF inválido!")
        return
    if any(u.cpf == cpf for u in usuarios):
        print("Já existe usuário com esse CPF!")
        return
    nome = input("Nome completo: ").strip()
    nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Endereço: ").strip()
    usuario = PessoaFisica(cpf, nome, nascimento, endereco)
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")

def criar_conta_corrente():
    cpf = input("CPF do usuário: ").strip()
    usuario = next((u for u in usuarios if u.cpf == cpf), None)
    if not usuario:
        print("Usuário não encontrado!")
        return
    numero = len(contas) + 1
    conta = ContaCorrente(usuario, numero)
    usuario.adicionar_conta(conta)
    contas.append(conta)
    print(f"Conta criada! Agência: {conta.agencia} Conta: {conta.numero}")

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Cliente: {conta.cliente.nome} (CPF: {conta.cliente.cpf})")

def exibir_extrato(conta):
    print("\nExtrato:")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for operacao in conta.historico.transacoes:
            print(operacao)
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")

def selecionar_conta():
    cpf = input("CPF do cliente: ").strip()
    usuario = next((u for u in usuarios if u.cpf == cpf), None)
    if not usuario or not usuario.contas:
        print("Usuário não encontrado ou sem conta!")
        return None
    return usuario.contas[0]

def main():
    while True:
        print("""
Selecione a opção:
1 - Criar usuário
2 - Criar conta corrente
3 - Depósito
4 - Saque
5 - Extrato
6 - Listar contas
7 - Sair
""")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            criar_conta_corrente()
        elif opcao == "3":
            conta = selecionar_conta()
            if conta:
                valor = float(input("Valor do depósito: "))
                conta.depositar(valor)
        elif opcao == "4":
            conta = selecionar_conta()
            if conta:
                valor = float(input("Valor do saque: "))
                conta.sacar(valor)
        elif opcao == "5":
            conta = selecionar_conta()
            if conta:
                exibir_extrato(conta)
        elif opcao == "6":
            listar_contas()
        elif opcao == "7":
            print("Obrigado e até logo!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
