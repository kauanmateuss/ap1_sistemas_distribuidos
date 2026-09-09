# Sistema Distribuído — gRPC e Protocol Buffers

Sistema distribuído utilizando a arquitetura cliente-servidor com gRPC e Protocol Buffers, desenvolvido para a atividade prática de Sistemas Distribuídos (UNIVASF).

O projeto implementa um gerenciador de tarefas simples, com um servidor central (gRPC) responsável por armazenar as tarefas em um banco SQLite, e uma aplicação cliente de linha de comando que consome os serviços remotos.

## Funcionalidades

O serviço `TarefaService`, definido em `protos/tarefa.proto`, expõe as seguintes operações:

- **CriarTarefa** — cria uma nova tarefa com título, retornando um ID único.
- **ListarTarefas** — retorna todas as tarefas cadastradas.
- **AtualizarTarefa** — atualiza o título e o status de conclusão de uma tarefa existente.
- **DeletarTarefa** — remove uma tarefa pelo ID.

## Estrutura do projeto
ap1_sistemas_distribuidos/
├── protos/
│ └── tarefa.proto # definicao do servico e das mensagens
├── gerenciador_tarefas/
│ ├── tarefa_server.py # implementacao do servidor gRPC
│ ├── tarefa_client.py # aplicacao cliente (menu interativo)
│ ├── tarefa_pb2.py # codigo gerado (mensagens)
│ ├── tarefa_pb2_grpc.py # codigo gerado (servico)
│ └── tarefas.db # banco sqlite (criado em tempo de execucao)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

## Requisitos

- Python 3.12+
- Docker Desktop (apenas para a demonstração com múltiplas máquinas)

## Executando localmente

**1. Criar e ativar o ambiente virtual:**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**2. Instalar as dependências:**

```powershell
pip install -r requirements.txt
```

**3. (Opcional) Regenerar o código a partir do `.proto`**, caso o arquivo `tarefa.proto` seja alterado:

```powershell
cd gerenciador_tarefas
python -m grpc_tools.protoc -I../protos --python_out=. --pyi_out=. --grpc_python_out=. ../protos/tarefa.proto
cd ..
```

**4. Rodar o servidor** (em um terminal, dentro de `gerenciador_tarefas`):

```powershell
cd gerenciador_tarefas
python tarefa_server.py
```

O servidor sobe na porta `80052` e exibe:

**5. Rodar o cliente** (em outro terminal, também dentro de `gerenciador_tarefas`):

```powershell
cd gerenciador_tarefas
python tarefa_client.py
```

O cliente exibe um menu interativo com as opções de listar, criar, atualizar e deletar tarefas.

## Demonstração com Docker (múltiplas máquinas)

Para simular o servidor e dois clientes rodando em máquinas diferentes, com IPs distintos na mesma rede, o projeto usa Docker Compose. São criados três containers em uma rede bridge dedicada (`172.28.0.0/16`):

| Serviço    | Papel         | IP            |
|------------|---------------|---------------|
| `servidor` | Servidor gRPC | `172.28.0.10` |
| `cliente1` | Cliente gRPC  | `172.28.0.11` |
| `cliente2` | Cliente gRPC  | `172.28.0.12` |

**1. Subir o servidor** (fica rodando em segundo plano):

```powershell
docker compose up -d --build servidor
```

Verificar se subiu corretamente:

```powershell
docker compose logs servidor
```

Deve aparecer `SERVIDOR GRPC RODANDO NA PORTA 80052...`.

**2. Rodar o cliente 1** (em um terminal — abre o menu interativo):

```powershell
docker compose run --rm cliente1
```

**3. Rodar o cliente 2** (em outro terminal, simultaneamente):

```powershell
docker compose run --rm cliente2
```

Como os dois clientes se conectam ao mesmo servidor (via `SERVER_ADDRESS=172.28.0.10:80052`), uma tarefa criada em um cliente aparece na listagem do outro — confirmando a comunicação distribuída entre "máquinas" diferentes.

**4. Verificar os IPs de cada container** (útil para a apresentação):

```powershell
docker network inspect ap1_sistemas_distribuidos_rede_tarefas
```

**5. Encerrar tudo ao final:**

```powershell
docker compose down
```

## Protocol Buffers vs JSON

O projeto utiliza Protocol Buffers como IDL (Interface Definition Language) para definir tanto as mensagens (`Tarefa`, `CreateTarefaRequest`, etc.) quanto o contrato do serviço (`TarefaService`). Em comparação com JSON:

- **Serialização binária**: Protobuf gera payloads menores e mais rápidos de serializar/desserializar do que o texto do JSON.
- **Schema tipado**: o `.proto` define um contrato fixo entre cliente e servidor, com tipos explícitos, reduzindo erros de integração.
- **Geração de código**: o compilador `protoc` gera automaticamente classes e stubs para cliente e servidor, eliminando parsing manual.
- **Legibilidade**: em contrapartida, JSON é texto puro, mais fácil de inspecionar manualmente, mas sem tipagem imposta e com maior overhead de tamanho.

