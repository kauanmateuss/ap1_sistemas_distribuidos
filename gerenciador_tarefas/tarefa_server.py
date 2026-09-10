import os
import sqlite3
import uuid
import grpc

from concurrent import futures

import tarefa_pb2
import tarefa_pb2_grpc

# pegando o caminho da raiz e definindo o caminho do arquivo do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "tarefas.db")

# funcao para conexao com o banco de dados sqlite
def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# funcao para inicializar o banco
def init_database():

    # criando a tabela se nao existir
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                descricao TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)


# implementacao do servico gRPC com os metodos definidos no arquivo .proto
class TarefaServicer(tarefa_pb2_grpc.TarefaServiceServicer):

    # metodo de criar uma nova tarefa
    def CreateTarefa(self, request, context):
        tarefa_id = str(uuid.uuid4())[:8]  # UUID curto

        # abrinco conexao com o banco para adicionar a nota tarefa no banco
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO tarefas (id, title, descricao, completed)
                VALUES (?, ?, ?, ?)
                """,
                (tarefa_id, request.title, request.descricao, 0),
            )

        # criando a resposta com a tarefa criada
        tarefa = tarefa_pb2.Tarefa(
            id=tarefa_id,
            title=request.title,
            descricao=request.descricao,
            completed=False
        )

        # retornando a resposta com a tarefa criada
        return tarefa_pb2.TarefaResponse(tarefa=tarefa)

    # metodo para listar as tarefas cadastradas no banco de dados
    def ListTarefas(self, request, context):
        # abrindo conexao com o banco para buscar as tarefaa
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, title, descricao, completed
                FROM tarefas
                ORDER BY rowid
                """
            ).fetchall()

        # resposta com a lista de tarefas cadastradas no banco de dados
        tarefas = [
            tarefa_pb2.Tarefa(
                id=row["id"],
                title=row["title"],
                descricao=row["descricao"],
                completed=bool(row["completed"]),
            )
            for row in rows
        ]

        return tarefa_pb2.ListTarefasResponse(tarefas=tarefas)


    # metodo para atualizar uma tarefa cadastrada no banco de dados
    def UpdateTarefa(self, request, context):
        # abrindo conexao com o banco para atualizar os dados da tarefa
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE tarefas
                SET title = ?, descricao = ?, completed = ?
                WHERE id = ?
                """,
                (request.title, request.descricao, request.completed, request.id),
            )

        # criando a resposta com a tarefa atualizada
        tarefa = tarefa_pb2.Tarefa(
            id=request.id,
            title=request.title,
            descricao=request.descricao,
            completed=request.completed
        )

        # retornando a resposta com a tarefa atualizada
        return tarefa_pb2.TarefaResponse(tarefa=tarefa)

    # metodo para deletar uma tarefa cadastrada no banco de dados
    def DeleteTarefa(self, request, context):

        with get_connection() as connection:
        #salvando o resultado da execução do comando DELETE para verificar se alguma linha foi afetada
            resultado = connection.execute(
                "DELETE FROM tarefas WHERE id = ?",
                (request.id,),
            )

            # verificando se alguma tarefa foi removida
            sucesso = resultado.rowcount > 0

        return tarefa_pb2.DeleteTarefaResponse(success=sucesso)

# Funcao para iniciar o servidor gRPC
def serve():
    # Inicializando o banco de dados
    init_database()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    tarefa_pb2_grpc.add_TarefaServiceServicer_to_server(TarefaServicer(), server)

    port = "80052"

    server.add_insecure_port(f"[::]:{port}")

    server.start()

    print(f"SERVIDOR GRPC RODANDO NA PORTA {port}...")

    server.wait_for_termination()

if __name__ == "__main__":
    serve()