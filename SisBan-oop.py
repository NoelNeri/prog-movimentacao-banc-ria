## Desafio Python - Rotinas bancárias com Orientação a Objeto

# Inclusão de classe abstrata e data/hora

## - Voltar a partir do DEBUG -  usar o video 2 a partir dos 13 minutos

import textwrap

from abc import ABC, abstractclassmethod,abstractproperty

from datetime import datetime

# CRIAÇÃO DE CLASSES =================================================================================================================
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, dt_nasc, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.dt_nasc = dt_nasc
        self.cpf = cpf

    #PessoaFisica herdou realizar_transacao e adicionar_conta da classe PAI que é Cliente

class Conta:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero_conta = numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero_conta):
        return cls(numero_conta, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_conta(self):
        return self._numero_conta

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, saque):
        saldo = self.saldo
        excedeu_saldo = saldo < saque

        if (excedeu_saldo):
            print ("@IE301 - Operação não concluída! Saldo insuficiente.")
            return False

        elif saque <= 0:
            print ("@IE302 - Operação não concluída! Saque negativou ou zerado.")
            return False

        else:
            self._saldo -= saque
            print ("#IS300 - Operação realizada com sucesso!")
            return True

    def depositar(self, deposito):
        if deposito > 0:
            self._saldo += deposito
            print ("#IS200 - Operação realizada com sucesso!")
            return True
        else:
            print ("@IE201 - Operação falhou. Valor de depósito negativo ou zerado.")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, lim_saque = 500, qtd_lim_saques=3):
        super().__init__(numero_conta, cliente)
        self._lim_saque = lim_saque
        self._qtd_lim_saques = qtd_lim_saques

    def sacar(self, saque):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
            )

        excedeu_limite = self._lim_saque < saque
        excedeu_saques = self._qtd_lim_saques <= numero_saques

        if excedeu_saques:
            print(f"@IE305 - Operação não concluída! Quatidade de {self._qtd_lim_saques} saques é o limite máximo para um mesmo dia.")
            return False
        elif excedeu_limite:
            print (f"@IE304 - Operação não concluída! Saque solicitado excede limite de {self._lim_saque} , válido para saques.")
            return False
        else:
            return super().sacar(saque)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C\C:\t\t{self.numero_conta}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
  ##              "data" : "03-05-2013 12:04:02",
                "data" : datetime.now().strftime('%d-%m-%Y %H:%M:%S')
  ##              "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")   ## tomando erro aqui
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass 

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)        

# CRIAÇÃO DE MÉTODOS =================================================================================================================
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

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf] 
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print(f"@IE101 - Cliente não possui conta. Você buscou o cliente {cliente}.")
        return


    # FIXME: Não permite cliente escolher conta. Pega sempre a primeira

    return cliente.contas[0]

def depositar(clientes):
    cpf = int(input("Informe o CPF do cliente: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"@IE208 - Cliente não encontrado. Você digitou {cpf}.")
        return

    valor = float(input("Informe o  valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = int(input("Informe o CPF do cliente: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"@IE308 - Cliente não encontrado. Você digitou {cpf}.")
        return

    valor = float(input("Informe o  valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
    

def exibir_extrato(clientes):
    cpf = int(input("Informe o CPF do cliente: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"@IE400 - Cliente não encontrado. Você digitou {cpf}.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print ("\n================ EXTRATO =================")

    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foi realizada qualquer transação nesta conta."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print ("==========================================")   

def criar_conta(numero_conta, clientes, contas):
    cpf = int(input("Informe o CPF do cliente: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(f"@IE000 - Cliente não encontrado. Você digitou {cpf}. Fluxo de criação de conta corrente encerrado.")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero_conta=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print(f"\n=== Conta {conta} criada com sucesso para o cpf {cliente.cpf}.")

def listar_contas(contas):
    if (contas):
        for conta in contas:
            print("=" * 100)
            print(textwrap.dedent(str(conta)))
    else:
        print ("@IE601 - Não há cotas a serem listadas.")
        
def criar_cliente(clientes):
    cpf = int(input("Informe o CPF (Somente números): "))
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print(f"\nJá existe cliente com o CPF {cpf}. Usuário não recriado.")
        return

    nome = input("Informe o nome completo: ")
    dt_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (Logradouro, nro - complemento - bairro - cidade/UF): ")

    cliente = PessoaFisica(nome=nome, dt_nasc=dt_nasc, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print ("#IS002 - Cliente criado com sucesso!")

def main():

    clientes = []
    contas = []

    while True:
        opcao = menu()

        if (opcao == "d"):
            depositar(clientes)

        elif (opcao == "s"):
            sacar(clientes)

        elif (opcao == "e"):
            exibir_extrato(clientes)

        elif (opcao == "nu"):
            criar_cliente(clientes)

        elif (opcao == "nc"):
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif (opcao == "lc"):
            listar_contas(contas)

        elif (opcao == "q"):
            break

        else:
            print (f"@IE501 - Opção inválida! Você digitou {opcao}.")

main()