class ContaBancaria:
    def __init__(self, titular, saldo):
        self.__titular = titular
        self.__saldo = saldo

    def depositar(self, valor):
        self.__saldo += valor

    def sacar(self, valor):
        if valor <= self.__saldo:
            self.__saldo -= valor
        else:
            print("Saldo insuficiente.")

    def exibir_saldo(self):
        print("Saldo atual:", self.__saldo)


conta = ContaBancaria("Rafael", 100)

conta.depositar(100)
conta.sacar(50)
conta.exibir_saldo()
