tarefas = []

def adicionar_tarefa():
    nome = input("Nome da tarefa: ")
    prioridade = input("Prioridade: ")

    tarefa = {
        "nome": nome,
        "prioridade": prioridade
    }

    tarefas.append(tarefa)
    print("Tarefa adicionada!")

def listar_tarefas():
    if len(tarefas) == 0:
        print("Nenhuma tarefa cadastrada.")
    else:
        for tarefa in tarefas:
            print("Tarefa:", tarefa["nome"])
            print("Prioridade:", tarefa["prioridade"])
            print("-----")

while True:
    print("\nMENU")
    print("1 - Adicionar tarefa")
    print("2 - Listar tarefas")
    print("0 - Sair")

    opcao = input("Escolha: ")

    if opcao == "1":
        adicionar_tarefa()
    elif opcao == "2":
        listar_tarefas()
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida")
