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

    # Métodos get e set para senha
    def get_senha(self):
        return "Senha protegida. Não pode ser acessada diretamente."

    def set_senha(self, senha_antiga, nova_senha):
        if self.__senha == senha_antiga:
            if len(str(nova_senha)) == 4 and str(nova_senha).isdigit():
                self.__senha = nova_senha
                print("Senha alterada com sucesso!")
            else:
                print("Nova senha inválida. Deve ser numérica e ter 4 dígitos.")
        else:
            print("Senha antiga incorreta.")

    # Método para validar a senha (já existia)
    def validar_senha(self, senha):
        return self.__senha == senha

    # Métodos get e set para saldo
    def get_saldo_corrente(self):
        return self.__saldo_corrente

    def set_saldo_corrente(self, valor):
        self.__saldo_corrente = valor

    def alterar_saldo_corrente(self, valor):
        self.__saldo_corrente += valor

    def depositar(self, valor):
        if valor >= 10.0:
            self.alterar_saldo_corrente(valor)
            print("Depósito realizado com sucesso!")
        else:
            print("O depósito deve ser no mínimo R$ 10,00.")

    def sacar(self, valor):
        if valor > self.__saldo_corrente:
            print("Saldo insuficiente.")
        else:
            self.alterar_saldo_corrente(-valor)
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

    def aplicar(self, conta_poupanca, valor):
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

    def alterar_saldo_poupanca(self, valor):
        self.__saldo_poupanca += valor

    def get_saldo_poupanca(self):
        return self.__saldo_poupanca

    def set_saldo_poupanca(self, valor):
        self.__saldo_poupanca = valor


# Funções utilitárias para entradas
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


# Função para criar conta
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


# Função para autenticar o usuário
def autenticar(conta):
    if conta.bloqueada:
        print("Conta bloqueada. Vá até uma agência para realizar o desbloqueio.")
        return False

    tentativas = 3
    while tentativas > 0:
        senha = input_int("Digite sua senha: ")
        if conta.validar_senha(senha):
            return True
        else:
            tentativas -= 1
            print(f"Senha incorreta. Tentativas restantes: {tentativas}")
    conta.bloqueada = True
    print("Conta bloqueada. Vá até uma agência para realizar o desbloqueio.")
    return False


# Menu principal
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
        print("7. Abrir nova conta")
        print("8. Sair")

        opcao = input_int("Escolha uma opção: ")

        if opcao == 1:
            valor = input_float("Digite o valor a depositar: ")
            conta_corrente.depositar(valor)

        elif opcao == 2:
            if autenticar(conta_corrente):
                valor = input_float("Digite o valor a sacar: ")
                conta_corrente.sacar(valor)

        elif opcao == 3:
            if autenticar(conta_corrente):
                valor = input_float("Digite o valor a aplicar para poupança: ")
                conta_corrente.aplicar(conta_poupanca, valor)

        elif opcao == 4:
            if autenticar(conta_corrente):
                valor = input_float("Digite o valor a resgatar da poupança: ")
                if valor <= conta_poupanca.get_saldo_poupanca():
                    conta_poupanca.alterar_saldo_poupanca(-valor)
                    conta_corrente.alterar_saldo_corrente(valor)
                    print(f"Resgate de R$ {valor:.2f} da poupança realizado com sucesso!")
                else:
                    print("Saldo insuficiente na poupança.")

        elif opcao == 5:
            print("\n=== Extrato ===")
            print(f"Titular: {conta_corrente.nome_titular}")
            print(f"Número da Conta: {conta_corrente.numero_conta}")
            print(f"Saldo Conta Corrente: R$ {conta_corrente.get_saldo_corrente():.2f}")
            print(f"Saldo Conta Poupança: R$ {conta_poupanca.get_saldo_poupanca():.2f}")
            print("================")

        elif opcao == 6:
            if autenticar(conta_corrente):
                senha_antiga = input_int("Digite sua senha antiga: ")
                nova_senha = input_int("Digite sua nova senha de 4 dígitos: ")
                conta_corrente.set_senha(senha_antiga, nova_senha)

        elif opcao == 7:
            print("Abrindo uma nova conta...")
            conta_corrente, conta_poupanca = criar_conta()

        elif opcao == 8:
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


menu()
