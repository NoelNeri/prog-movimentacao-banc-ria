## Desafio Python - Extrato

menu = """

[d] Deposito
[s] Saque
[e] Extrato
[q] Sair

"""

saldo = 0
deposito = 0
saque = 0
valor_lim_saque = 500
extrato = ""
numero_saques = 0
qtd_lim_saque = 3

while True:

    opcao = input(menu)

    if (opcao == "d"):

        deposito = float(input("Informe o valor do depósito: "))

        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"

        else:
            print ("Operação falhou. Valor de depósito negativo ou zerado.")


    elif (opcao == "s"):

        if (numero_saques >= qtd_lim_saque): # Excedeu a quantidade de saque para um mesmo dia
            print(f"Operação não concluída! Quatidade de {qtd_lim_saque} saques excede limite válido para um mesmo dia.")

        else:

            saque = float(input("Informe o valor do saque: "))

            if (saldo < saque): # Excedeu o saldo disponível
                print ("Operação não concluída! Saldo insuficiente.")

            elif (valor_lim_saque < saque): # Excedeu o limite válido para saque único
                print (f"Operação não concluída! Saque solicitado excede limite de {valor_lim_saque} , válido para saques.")
            
            elif (saque <= 0): # Valor do saque é negativo ou zero
                print ("Operação não concluída! Saque negativou ou zerado.")

            else:
                saldo -= saque
                extrato += f"Saque: R$ {saque:.2f}\n"
                numero_saques += 1

    elif (opcao == "e"):

        print ("=========== EXTRATO ============")

        print ("Não foram realizadas movimentações" if not extrato else extrato)
        print (f"\nSaldo:  R$ {saldo:.2f}")

        print ("================================")

    elif (opcao == "q"):
        print ("Fim do programa.")

        break

    else:
        print (f"Opção inválida! Você digitou {opcao}.")


