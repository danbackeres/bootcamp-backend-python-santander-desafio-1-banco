import os

# Função de mensagem
def mensagem(str):
    print()
    print(str)
    print()

# Função de saque (apenas argumentos nomeados)
def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        mensagem("Saldo insuficiente para saque!")
    elif valor > limite:
        mensagem("Valor do saque excede o limite permitido!")
    elif numero_saques >= limite_saques:
        mensagem("Limite de saques diários atingido!")
    elif valor <= 0:
        mensagem("Valor inválido para saque!")
    else:
        saldo -= valor
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
        mensagem("Saque realizado com sucesso!")
    return saldo, extrato, numero_saques

# Função de depósito (apenas argumentos posicionais)
def deposito(saldo, valor, extrato, /):
    if valor <= 0:
        mensagem("Valor inválido para depósito!")
    else:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        mensagem("Depósito realizado com sucesso!")
    return saldo, extrato

# Função de extrato (posicional e nomeado)
def exibir_extrato(saldo, *, extrato):
    print("\nExtrato:")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for operacao in extrato:
            print(operacao)
    print(f"\nSaldo atual: R$ {saldo:.2f}")

# Função para criar usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    if not cpf.isdigit() or len(cpf) != 11:
        mensagem("CPF inválido! Deve conter 11 dígitos numéricos.")
        return
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            mensagem("Já existe usuário com esse CPF!")
            return
    nome = input("Informe o nome completo: ").strip()
    nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()
    usuarios.append({
        "nome": nome,
        "data_nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    mensagem("Usuário criado com sucesso!")

# Função para criar conta corrente
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if not usuario:
        mensagem("Usuário não encontrado! Cadastre o usuário primeiro.")
        return
    contas.append({
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario
    })
    mensagem(f"Conta criada com sucesso! Agência: {agencia} Conta: {numero_conta}")

def main():
    AGENCIA = "0001"
    usuarios = []
    contas = []
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3
    numero_conta = 1

    while True:
        try:
            menu = f"""
Selecione a opção:
(1) - Depósito
(2) - Saque
(3) - Extrato
(4) - Criar usuário
(5) - Criar conta corrente
(6) - Listar contas
(7) - Sair
"""
            print(' Menu '.center(50, ':'))
            print(menu)
            opcao_selecionada = input("Digite a opção numérica: ")

            if not opcao_selecionada:
                raise ValueError('Opção inválida!')
                
            opcao_selecionada = int(opcao_selecionada)

            if opcao_selecionada == 7:
                mensagem("Obrigado e até logo. =D ")
                break

            elif opcao_selecionada == 1:
                valor = input("Digite o valor do depósito: ")
                if not valor or not valor.replace('.', '', 1).isdigit():
                    raise ValueError("Digite apenas valores numéricos!")
                saldo, extrato = deposito(saldo, float(valor), extrato)

            elif opcao_selecionada == 2:
                valor = input("Digite o valor do saque: ")
                if not valor or not valor.replace('.', '', 1).isdigit():
                    raise ValueError("Digite apenas valores numéricos!")
                saldo, extrato, numero_saques = saque(
                    saldo=saldo,
                    valor=float(valor),
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES
                )

            elif opcao_selecionada == 3:
                exibir_extrato(saldo, extrato=extrato)

            elif opcao_selecionada == 4:
                criar_usuario(usuarios)

            elif opcao_selecionada == 5:
                criar_conta(AGENCIA, numero_conta, usuarios, contas)
                numero_conta += 1

            elif opcao_selecionada == 6:
                print("\nContas cadastradas:")
                for conta in contas:
                    print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Usuário: {conta['usuario']['nome']} (CPF: {conta['usuario']['cpf']})")
                print()

            else:
                raise ValueError("Opção inválida!")

        except ValueError as e:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'ERROR: {str(e)}')

if __name__ == "__main__":
    main()
