# código por Loxfusion-LM

from datetime import date

menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Cadastrar Usuário
[5] Cadastrar Conta
[6] Mostrar Contas
[7] Sair

=> """

# Variáveis de controle
usuarios = []
contas = []
numero_conta = 1
AGENCIA = "0001"
limite_saque = 500.0
limite_diario = 3

# Pessoa Fisica
class PessoaFisica:
    def __init__(self, cpf: str, nome: str, data_nascimento: date):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# Cliente
class Cliente(PessoaFisica):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(cpf, nome, data_nascimento)
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Histórico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Transação
class Transacao:
    def registrar(self, conta):
        pass

# Deposíto
class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(f"Depósito de R$ {self.valor:.2f} realizado com sucesso")
        print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso")

# Saque
class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        if self.valor <= 0:
            print("Operação falhou! O valor informado é inválido.")
        elif self.valor > conta.saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif self.valor > limite_saque:
            print("Operação falhou! O valor do saque excede o limite.")
        elif conta.numero_saques >= limite_diario:
            print("Operação falhou! Número máximo de saques excedido.")
        else:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(f"Saque de R$ {self.valor:.2f} realizado com sucesso")
            conta.numero_saques += 1
            print(f"Saque de R$ {self.valor:.2f} realizado com sucesso")

# Conta
class Conta:
    def __init__(self, numero: int, agencia: str, cliente: Cliente):
        self.numero = numero
        self.agencia = agencia
        self.saldo = 0.0
        self.cliente = cliente
        self.historico = Historico()
        self.numero_saques = 0

# Conta corrente
class ContaCorrente(Conta):
    def __init__(self, numero: int, agencia: str, cliente: Cliente, limite: float, limite_saques: int):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

# Buscar conta por CPF
def buscar_conta_por_cpf(cpf):
    for conta in contas:
        if conta.cliente.cpf == cpf:
            return conta
    return None

# Criar usuário
def criar_usuario(nome, data_nascimento, cpf, endereco):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            print("Usuário já cadastrado!")
            return
    novo_cliente = Cliente(cpf, nome, date(*map(int, data_nascimento.split('/')[::-1])), endereco)
    usuarios.append(novo_cliente)
    print("Usuário cadastrado com sucesso!")

# Criar conta corrente
def criar_conta(cpf):
    global numero_conta
    usuario = None
    for u in usuarios:
        if u.cpf == cpf:
            usuario = u
            break
    if usuario:
        nova_conta = ContaCorrente(numero_conta, AGENCIA, usuario, limite=limite_saque, limite_saques=limite_diario)
        usuario.adicionar_conta(nova_conta)
        contas.append(nova_conta)
        print(f"Conta {numero_conta} criada com sucesso!")
        numero_conta += 1
    else:
        print("Usuário não encontrado. Cadastro não realizado.")

# Mostrar contas criadas
def mostrar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        print("\n=========== Contas Cadastradas ===========")
        for conta in contas:
            print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Usuário: {conta.cliente.nome}")
        print("==========================================")

# Loop principal
while True:
    opcao = input(menu).lower()
    
    if opcao == "1":
        cpf = input("Informe o CPF do usuário: ")
        conta = buscar_conta_por_cpf(cpf)
        if conta:
            valor = float(input("Informe o valor do depósito: "))
            deposito = Deposito(valor)
            conta.cliente.realizar_transacao(conta, deposito)
        else:
            print("Conta não encontrada. Verifique o CPF informado.")
    
    elif opcao == "2":
        cpf = input("Informe o CPF do usuário: ")
        conta = buscar_conta_por_cpf(cpf)
        if conta:
            valor = float(input("Informe o valor do saque: "))
            saque = Saque(valor)
            conta.cliente.realizar_transacao(conta, saque)
        else:
            print("Conta não encontrada. Verifique o CPF informado.")
    
    elif opcao == "3":
        cpf = input("Informe o CPF do usuário: ")
        conta = buscar_conta_por_cpf(cpf)
        if conta:
            print("\n================ Extrato ================")
            if not conta.historico.transacoes:
                print("Não foram realizadas movimentações.")
            else:
                for movimento in conta.historico.transacoes:
                    print(movimento)
            print(f"\nSaldo: R$ {conta.saldo:.2f}")
            print("==========================================")
        else:
            print("Conta não encontrada. Verifique o CPF informado.")
    
    elif opcao == "4":
        nome = input("Nome: ")
        data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
        cpf = input("CPF (apenas números): ")
        endereco = input("Endereço (logradouro, n° - bairro - cidade/sigla estado): ")
        criar_usuario(nome, data_nascimento, cpf, endereco)
    
    elif opcao == "5":
        cpf = input("Informe o CPF do usuário: ")
        criar_conta(cpf)
    
    elif opcao == "6":
        mostrar_contas()

    elif opcao == "7":
        print("Obrigado por utilizar o sistema. Até logo!")
        break
    
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")


