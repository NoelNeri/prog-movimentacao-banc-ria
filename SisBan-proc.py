## Desafio Python - Rotinas bancárias com proc

import textwrap

def menu():
    menu = """\n
    ================= MENU =================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar contas
    [nu]\tNovo Usuário
    [q]\tSair
    ==> """
    return input(textwrap.dedent(menu))

def depositar(saldo, deposito, extrato):

    if deposito > 0:
        saldo += deposito
        extrato += f"Depósito:\tR$ {deposito:.2f}\n"
        print ("#IS000 - Operação realizada com sucesso!")
    else:
        print ("@IE101 - Operação falhou. Valor de depósito negativo ou zerado.")

    return saldo, extrato

def sacar(numero_saques, /, *, saldo, saque, extrato, limite, lim_saque):
    excedeu_saques = numero_saques > lim_saque
    excedeu_saldo = saldo < saque
    excedeu_limite = limite < saque

    if (excedeu_saques): # Excedeu a quantidade de saque para um mesmo dia
        print(f"@IE102 - Operação não concluída! Quatidade de {numero_saques} saques é o limite máximo para um mesmo dia.")

    elif (excedeu_saldo): # Excedeu o saldo disponível
        print ("@IE103 - Operação não concluída! Saldo insuficiente.")

    elif (excedeu_limite): # Excedeu o limite válido para saque único
        print (f"@IE104 - Operação não concluída! Saque solicitado excede limite de {limite} , válido para saques.")
        
    elif (saque <= 0): # Valor do saque é negativo ou zero
        print ("@IE105 - Operação não concluída! Saque negativou ou zerado.")

    else:
        saldo -= saque
        extrato += f"Saque:\t\tR$ {saque:.2f}\n"
        numero_saques += 1
        print ("#IS001 - Operação realizada com sucesso!")
        

    return saldo, extrato, numero_saques

def exibir_extrato(saldo,/,*,extrato):
    print ("=========== EXTRATO ============")

    print ("Não foram realizadas movimentações" if not extrato else extrato)
    print (f"\nSaldo:\t\tR$ {saldo:.2f}")

    print ("================================")

def criar_usuario(usuarios):
    cpf = int(input("Informe o CPF (Somente números): "))
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(f"\nJá existe usuário com o CPF {cpf}. Usuário não recriado.")
        return

    nome = input("Informe o nome completo: ")
    dt_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (Logradouro, nro - complemento - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "dt_nasc": dt_nasc,
        "cpf": cpf,
        "endereco": endereco})

    print ("#IS002 - Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf] 
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = int(input("Informe o cpf do usuário (apenas números): "))
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia,
                "numero_conta": numero_conta,
                "usuario": usuario}

    print(f"Usuário com cpf {cpf} não encontrado. Processo de criação de conta encerrado sem criar nova conta.")

def listar_contas(contas):
    if contas:
        for conta in contas:
            linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

    print("@IE106 - Não há contas a serem listadas.")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    VAL_LIM_SAQUE = 500

    saldo = 0
    deposito = 0
    saque = 0
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    nova_conta = 1

    while True:

        opcao = menu()

        if (opcao == "d"):

            deposito = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, deposito, extrato)

        elif (opcao == "s"):

            saque = float(input("Informe o valor do saque: "))

            saldo, extrato, numero_saques = sacar(
                numero_saques,
                saldo=saldo,
                saque=saque,
                extrato=extrato,
                limite=VAL_LIM_SAQUE,
                lim_saque=LIMITE_SAQUES
            )

        elif (opcao == "e"):
            exibir_extrato(saldo,extrato=extrato)

        elif (opcao == "nu"):
            criar_usuario(usuarios)

        elif (opcao == "nc"):
            numero_conta = nova_conta
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                nova_conta += 1
                
        elif (opcao == "lc"):
            listar_contas(contas)
        
        elif (opcao == "q"):
            print ("Fim do programa.")

            break

        else:
            print (f"@IE107 - Opção inválida! Você digitou {opcao}.")

main()