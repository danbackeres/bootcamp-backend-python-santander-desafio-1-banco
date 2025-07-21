from abc import ABC, abstractmethod
from datetime import datetime
from functools import wraps
import os

# Decorador de LOG
def log_transacao(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        if resultado:
            log_message = (
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"Função: {func.__name__} | "
                f"Args: {args} | Kwargs: {kwargs} | "
                f"Retorno: {resultado}\n"
            )
            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(log_message)
        return resultado
    return wrapper
    
def log_geral(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        log_message = (
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Ação: {func.__name__} | Args: {args} | Kwargs: {kwargs} | Retorno: {resultado}\n"
        )
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(log_message)
        return resultado
    return wrapper

   
# Iterador    
class ContaIterador:
    def __init__(self, contas):
        self._contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._contas):
            raise StopIteration
        conta = self._contas[self._index]
        self._index += 1
        return {
            "agencia": conta.agencia,
            "numero": conta.numero,
            "cliente": conta.cliente.nome,
            "cpf": conta.cliente.cpf,
            "saldo": conta.saldo
        }    

# Histórico de transações
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, descricao):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transacoes.append({"descricao": descricao, "data": data})

    def gerar_relatorio(self, tipo=None):
        for transacao in self.transacoes:
            if tipo is None or tipo.lower() in transacao["descricao"].lower():
                yield f"{transacao['data']} - {transacao['descricao']}"

# Interface de transação
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Depósito
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
        
    def __repr__(self):
        return f"<{self.__class__.__name__}: valor=R$ {self.valor:.2f}>"    
        
    @log_transacao
    def registrar(self, conta):
        if conta.limite_transacoes_excedido():
            print("Você excedeu o limite diário de 10 transações.")
            return False
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
        
    def __repr__(self):
        return f"<{self.__class__.__name__}: valor=R$ {self.valor:.2f}>"    

    @log_transacao
    def registrar(self, conta):
        if conta.limite_transacoes_excedido():
            print("Você excedeu o limite diário de 10 transações.")
            return False
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
        
    def __repr__(self):
        return f"<{self.__class__.__name__}: nome={self.nome}, cpf={self.cpf}, nascimento={self.data_nascimento}>"
    
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

    def transacoes_hoje(self):
        hoje = datetime.now().date()
        return [
            t for t in self.historico.transacoes
            if datetime.strptime(t["data"], "%Y-%m-%d %H:%M:%S").date() == hoje
        ]

    def limite_transacoes_excedido(self):
        return len(self.transacoes_hoje()) >= 10

# Conta Corrente
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0
        
    def __repr__(self):
        return f"<{self.__class__.__name__}: agencia={self.agencia}, numero={self.numero}, saldo={self.saldo:.2f}, cliente={self.cliente.nome}>"

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

usuarios = []
contas = []

def exibir_relatorio(conta):
    print("\n--- Relatório de Transações ---")
    tipo = input("Filtrar por tipo (ex: saque, depósito) ou deixe em branco para todas: ").strip()
    relatorio = conta.historico.gerar_relatorio(tipo if tipo else None)

    tem_transacoes = False
    for transacao in relatorio:
        print(transacao)
        tem_transacoes = True

    if not tem_transacoes:
        print("Nenhuma transação encontrada com esse filtro.")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")

@log_geral
def criar_usuario():
    cpf = input("CPF (11 dígitos): ").strip()
    if not cpf.isdigit() or len(cpf) != 11:
        print("CPF inválido!")
        return None
    if any(u.cpf == cpf for u in usuarios):
        print("Já existe usuário com esse CPF!")
        return None
    nome = input("Nome completo: ").strip()
    nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Endereço: ").strip()
    usuario = PessoaFisica(cpf, nome, nascimento, endereco)
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")
    return usuario

@log_geral
def criar_conta_corrente():
    cpf = input("CPF do usuário: ").strip()
    usuario = next((u for u in usuarios if u.cpf == cpf), None)
    if not usuario:
        print("Usuário não encontrado!")
        return None
    numero = len(contas) + 1
    conta = ContaCorrente(usuario, numero)
    usuario.adicionar_conta(conta)
    contas.append(conta)
    print(f"Conta criada! Agência: {conta.agencia} Conta: {conta.numero}")
    return conta 


def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for info in ContaIterador(contas):
        print(f"Agência: {info['agencia']}, Conta: {info['numero']}, Cliente: {info['cliente']} (CPF: {info['cpf']})")

def exibir_extrato(conta):
    print("\nExtrato:")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"{transacao['data']} - {transacao['descricao']}")
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
8 - Relatório de transações
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
        elif opcao == "8":
            conta = selecionar_conta()
            if conta:
                exibir_relatorio(conta)
        elif opcao == "7":
            print("Obrigado e até logo!")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
