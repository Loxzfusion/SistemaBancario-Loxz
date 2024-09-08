# Definição do menu do sistema bancário

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

# Função para buscar conta por CPF
def buscar_conta_por_cpf(cpf):
    for conta in contas:
        if conta["usuario"]["cpf"] == cpf:
            return conta
    return None

# Função para sacar, argumentos keyword only
def sacar(*, conta, valor):
    saldo = conta["saldo"]
    extrato = conta["extrato"]
    numero_saques = conta["numero_saques"]

    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    elif valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite_saque:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_diario:
        print("Operação falhou! Número máximo de saques excedido.")
    else:
        conta["saldo"] -= valor
        conta["extrato"].append(f"Saque: R$ {valor:.2f}")
        conta["numero_saques"] += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

# Função para depositar, argumentos positional only
def depositar(conta, valor, /):
    saldo = conta["saldo"]
    extrato = conta["extrato"]

    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"].append(f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

# Função para exibir extrato, positional e keyword arguments
def exibir_extrato(conta, /):
    saldo = conta["saldo"]
    extrato = conta["extrato"]

    print("\n================ Extrato ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for movimento in extrato:
            print(movimento)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Função para criar usuário
def criar_usuario(nome, data_nascimento, cpf, endereco):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Usuário já cadastrado!")
            return
    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário cadastrado com sucesso!")

# Função para criar conta corrente
def criar_conta(cpf):
    global numero_conta
    usuario = None
    for u in usuarios:
        if u["cpf"] == cpf:
            usuario = u
            break
    if usuario:
        contas.append({
            "agencia": AGENCIA,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0.0,
            "extrato": [],
            "numero_saques": 0
        })
        print(f"Conta {numero_conta} criada com sucesso!")
        numero_conta += 1
    else:
        print("Usuário não encontrado. Cadastro não realizado.")

# Função para mostrar as contas criadas
def mostrar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        print("\n=========== Contas Cadastradas ===========")
        for conta in contas:
            print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Usuário: {conta['usuario']['nome']}")
        print("==========================================")

# Loop principal
while True:
    opcao = input(menu).lower()
    
    if opcao == "1":
        cpf = input("Informe o CPF do usuário: ")
        conta = buscar_conta_por_cpf(cpf)
        if conta:
            valor = float(input("Informe o valor do depósito: "))
            depositar(conta, valor)
        else:
            print("Conta não encontrada. Verifique o CPF informado.")
    
    elif opcao == "2":
        cpf = input("Informe o CPF do usuário: ")
        conta = buscar_conta_por_cpf(cpf)
        if conta:
            valor = float(input("Informe o valor do saque: "))
            sacar(conta=conta, valor=valor)
        else:
            print("Conta não encontrada. Verifique o CPF informado.")
    
    elif opcao == "3":
        cpf = input("Informe o CPF do usuário: ")
        conta = buscar_conta_por_cpf(cpf)
        if conta:
            exibir_extrato(conta)
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



        