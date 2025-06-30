import os

def mensagem(str):
    print()
    print(str)
    print()
    
saldo = 0

while True:
    try:

        menu = f"""Selecione a opção:
        (1) - Depósito
        (2) - Saque
        (3) - Extrato
        (4) - Sair"""

        print(' Menu '.center(50, ':'))
        print(menu)
        opcao_selecionada = input("Digite a opção numérica: ")

        if not opcao_selecionada:
            raise ValueError('Opção inválida!')
            
        opcao_selecionada = int(opcao_selecionada)

        if opcao_selecionada == 4:
            mensagem("Obrigado e até logo. =D ")
            break;
            
        if opcao_selecionada == 1:
            valor = input("Digite o valor do deposito: ")
            if not valor:
                raise ValueError("Valor inválido!")
            if not valor.isdigit():
                raise ValueError("Digite apenas valores numéricos!");
            saldo += int(valor)
            mensagem("Depósito realizado com sucesso! ")
            
        if opcao_selecionada == 2:
            valor = input("Digite o valor do saque: ")
            if not valor:
                raise ValueError("Valor inválido!")
            if not valor.isdigit():
                raise ValueError("Digite apenas valores numéricos!");
            valor = int(valor)    
            if saldo < valor:
                raise ValueError("Saldo insuficiente para saque!");
            saldo -= valor
            mensagem("Saque realizado com sucesso! ")
            
        if opcao_selecionada == 3:
            mensagem(f"Seu saldo é de R$ {saldo:.2f}")
        
        
    except ValueError as e:
        os.system('cls')
        print(f'ERROR: {str(e)}')