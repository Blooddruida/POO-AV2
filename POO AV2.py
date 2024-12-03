import random

# Registro de contas
numero_contas_existentes = set()


def gerar_numero_conta():
    while True:
        numero = random.randint(100, 999)
        if numero not in numero_contas_existentes:
            numero_contas_existentes.add(numero)
            return numero


class ContaCorrente:
    def __init__(self, nome_titular, senha):
        self.nome_titular = nome_titular
        self.numero_conta = gerar_numero_conta()
        self.__senha = senha
        self.__saldo_corrente = 0.0
        self.bloqueada = False

    def validar_senha(self, senha):
        return self.__senha == senha

    def set_senha(self, nova_senha):
        if len(str(nova_senha)) == 4 and str(nova_senha).isdigit():
            self.__senha = nova_senha
            print("Senha alterada com sucesso!")
        else:
            print("A nova senha deve ter exatamente 4 dígitos numéricos.")

    def get_saldo_corrente(self):
        return self.__saldo_corrente

    def alterar_saldo_corrente(self, valor):
        self.__saldo_corrente += valor

    def depositar(self, valor):
        if valor >= 10.0:
            self.alterar_saldo_corrente(valor)
            print("Depósito realizado com sucesso!")
        else:
            print("O depósito deve ser no mínimo R$ 10,00.")

    def sacar(self, senha, valor):
        if not self.validar_senha(senha):
            print("Senha incorreta. Não foi possível realizar o saque.")
            return
        if valor > self.__saldo_corrente:
            print("Saldo insuficiente.")
        else:
            self.alterar_saldo_corrente(-valor)
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

    def aplicar(self, senha, conta_poupanca, valor):
        if not self.validar_senha(senha):
            print("Senha incorreta. Não foi possível realizar a aplicação.")
            return
        if valor > self.__saldo_corrente:
            print("Saldo insuficiente para aplicação.")
        else:
            self.alterar_saldo_corrente(-valor)
            conta_poupanca.alterar_saldo_poupanca(valor)
            print(f"Aplicação de R$ {valor:.2f} para poupança realizada com sucesso!")


class ContaPoupanca:
    def __init__(self, nome_titular):
        self.nome_titular = nome_titular
        self.__saldo_poupanca = 0.0

    def get_saldo_poupanca(self):
        return self.__saldo_poupanca

    def alterar_saldo_poupanca(self, valor):
        self.__saldo_poupanca += valor

    def resgatar(self, senha, conta_corrente, valor):
        if not conta_corrente.validar_senha(senha):
            print("Senha incorreta. Não foi possível realizar o resgate.")
            return
        if valor > self.__saldo_poupanca:
            print("Saldo insuficiente na poupança.")
        else:
            self.alterar_saldo_poupanca(-valor)
            conta_corrente.alterar_saldo_corrente(valor)
            print(f"Resgate de R$ {valor:.2f} da poupança realizado com sucesso!")

    def extrato(self, senha, conta_corrente):
        if not conta_corrente.validar_senha(senha):
            print("Senha incorreta. Não foi possível exibir o extrato.")
            return
        print("\n=== Extrato ===")
        print(f"Titular: {conta_corrente.nome_titular}")
        print(f"Conta: {conta_corrente.numero_conta}")
        print(f"Saldo Conta Corrente: R$ {conta_corrente.get_saldo_corrente():.2f}")
        print(f"Saldo Poupança: R$ {self.get_saldo_poupanca():.2f}")
        print("================")


def input_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0:
                print("O valor deve ser positivo.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Digite um número.")


def input_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def criar_conta():
    nome = input("Digite o nome completo do titular: ")
    while True:
        senha = input("Crie uma senha numérica de 4 dígitos: ")
        if len(senha) == 4 and senha.isdigit():
            senha = int(senha)
            break
        else:
            print("A senha deve ter exatamente 4 dígitos numéricos.")

    conta_corrente = ContaCorrente(nome, senha)
    conta_poupanca = ContaPoupanca(nome)

    while True:
        deposito_inicial = input_float("Faça o depósito inicial (mínimo R$ 10,00): ")
        if deposito_inicial >= 10:
            conta_corrente.depositar(deposito_inicial)
            print(f"Conta corrente criada com sucesso! Número da conta: {conta_corrente.numero_conta}")
            return conta_corrente, conta_poupanca
        else:
            print("O depósito inicial deve ser no mínimo R$ 10,00.")


def menu():
    conta_corrente, conta_poupanca = criar_conta()

    while True:
        print("\n=== Menu ===")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Aplicar para Poupança")
        print("4. Resgatar da Poupança")
        print("5. Extrato")
        print("6. Alterar Senha")
        print("7. Sair")

        opcao = input_int("Escolha uma opção: ")

        if opcao == 1:
            valor = input_float("Digite o valor a depositar: ")
            conta_corrente.depositar(valor)

        elif opcao == 2:
            senha = input_int("Digite sua senha: ")
            valor = input_float("Digite o valor a sacar: ")
            conta_corrente.sacar(senha, valor)

        elif opcao == 3:
            senha = input_int("Digite sua senha: ")
            valor = input_float("Digite o valor a aplicar para poupança: ")
            conta_corrente.aplicar(senha, conta_poupanca, valor)

        elif opcao == 4:
            senha = input_int("Digite sua senha: ")
            valor = input_float("Digite o valor a resgatar da poupança: ")
            conta_poupanca.resgatar(senha, conta_corrente, valor)

        elif opcao == 5:
            senha = input_int("Digite sua senha: ")
            conta_poupanca.extrato(senha, conta_corrente)

        elif opcao == 6:
            nova_senha = input_int("Digite a nova senha (4 dígitos): ")
            conta_corrente.set_senha(nova_senha)

        elif opcao == 7:
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


menu()