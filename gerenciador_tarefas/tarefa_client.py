import sys
import grpc

import tarefa_pb2
import tarefa_pb2_grpc

def mostrar_menu():
    print("\n===== GERENCIADOR DE TAREFAS ====== ")   # Se tiverem um nome mais criativo
    print("1 - LISTAR TAREFAS")
    print("2 - CRIAR TAREFA")
    print("0 - SAIR")
    print("=====================================\n")


def run():

    # Criando o canal de comunicacao e o stub para interagir com o servidor
    channel = grpc.insecure_channel("localhost:80052")
    stub = tarefa_pb2_grpc.TarefaServiceStub(channel)

    # laco principal do cliente
    while True:
        mostrar_menu()
        opcao = input("ESCOLHA UMA OPCAO ABAIXO: ").strip()

        # Verificando a opcao escolhida pelo usuario
        if opcao == "1":

            response = stub.ListTarefas(tarefa_pb2.Empty())   # Chamando o metodo ListTarefas

            # se não tiver nenhuma tarefa cadastrada
            if not response.tarefas:
                print("NENHUMA TAREFA CADASTRADA.")
            else:
                print("\nTAREFAS CADASTRADAS:\n")
                print(response.tarefas)
                # for t in response.tarefas:
                    # print(f"ID: {t.id} | {t.title}\n")

        elif opcao == "2":
            # Criando uma nova tarefa
            titulo = input("DIGITE O TITULO DA TAREFA: ").strip()

            # se o usuario nao digitou nada
            if not titulo:
                print("ERRO! TITULO NAO PODE SER VAZIO. TENTE NOVAMENTE\n")
                continue

            # chamando o metodo para criar a tarefa com o titulo informado
            response = stub.CreateTarefa(tarefa_pb2.CreateTarefaRequest(title=titulo))
            print(f"Tarefa criada! ID: {response.tarefa.id} - '{response.tarefa.title}'")

        elif opcao == "0":
            print("ENCERRANDO...")
            channel.close()
            sys.exit(0)

        else:
            print("OPCAO INVALIDA. TENTE NOVAMENTE.")


# Rodando o cliente
run()