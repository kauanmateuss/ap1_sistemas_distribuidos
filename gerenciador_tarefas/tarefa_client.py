import os
import sys
import grpc

import tarefa_pb2
import tarefa_pb2_grpc

def mostrar_menu():
    print("\n===== GERENCIADOR DE TAREFAS ====== ")   # Se tiverem um nome mais criativo
    print("1 - LISTAR TAREFAS")
    print("2 - CRIAR TAREFA")
    print("3 - ATUALIZAR TAREFA")
    print("4 - DELETAR TAREFA")
    print("0 - SAIR")
    print("=====================================\n")


def run():

    # Criando o canal de comunicacao e o stub para interagir com o servidor
    server_address = os.environ.get("SERVER_ADDRESS", "localhost:80052")
    channel = grpc.insecure_channel(server_address)
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
                print("NENHUMA TAREFA CADASTRADA.\n")
            else:
                print("\nTAREFAS CADASTRADAS:\n")
                print(response.tarefas)
                # for t in response.tarefas:
                    # print(f"ID: {t.id} | {t.title}\n")

        elif opcao == "2":
            # Criando uma nova tarefa
            titulo = input("DIGITE O TITULO DA TAREFA: ").strip()
            descricao = input("DIGITE UMA DESCRICAO PARA A TAREFA: ").strip()

            # se o usuario nao digitou nada
            if not titulo:
                print("ERRO! TITULO NAO PODE SER VAZIO. TENTE NOVAMENTE\n")
                continue

            # chamando o metodo para criar a tarefa com o titulo informado
            response = stub.CreateTarefa(tarefa_pb2.CreateTarefaRequest(title=titulo, descricao=descricao, completed=False))
            print(f"\nTAREFA CRIADA! ID: {response.tarefa.id} \nTITULO:'{response.tarefa.title}' \nDESCRICAO:'{response.tarefa.descricao}' \nCONCLUIDA: {response.tarefa.completed}\n")

        elif opcao == "3":
            # Atualizando uma tarefa cadastrada
            tarefa_id = input("DIGITE O ID DA TAREFA: ").strip()
            titulo = input("NOVO TITULO: ").strip()
            descricao = input("NOVA DESCRICAO: ").strip()
            concluida = input("CONCLUIDA? (s/n): ").strip().lower() == "s"

            # chamando o metodo para atualizar a tarefa informada
            response = stub.UpdateTarefa(tarefa_pb2.UpdateTarefaRequest(id=tarefa_id, title=titulo, descricao=descricao, completed=concluida))
            print(f"\nTAREFA ATUALIZADA! ID: {response.tarefa.id} \nTITULO:'{response.tarefa.title}' \nDESCRICAO:'{response.tarefa.descricao}' \nCONCLUIDA: {response.tarefa.completed}\n")

        elif opcao == "4":
            # Deletando uma tarefa cadastrada
            tarefa_id = input("DIGITE O ID DA TAREFA A DELETAR: ").strip()

            # chamando o metodo para deletar a tarefa informada
            response = stub.DeleteTarefa(tarefa_pb2.TarefaRequest(id=tarefa_id))
            if response.success:
                print("Tarefa deletada com sucesso.")
            else:
                print("Tarefa nao encontrada.")

        elif opcao == "0":
            print("ENCERRANDO...")
            channel.close()
            sys.exit(0)

        else:
            print("OPCAO INVALIDA. TENTE NOVAMENTE.\n")


# Rodando o cliente
run()