from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Tarefa(_message.Message):
    __slots__ = ("id", "title", "descricao", "completed")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRICAO_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    descricao: str
    completed: bool
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., descricao: _Optional[str] = ..., completed: _Optional[bool] = ...) -> None: ...

class CreateTarefaRequest(_message.Message):
    __slots__ = ("title", "descricao", "completed")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRICAO_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    title: str
    descricao: str
    completed: bool
    def __init__(self, title: _Optional[str] = ..., descricao: _Optional[str] = ..., completed: _Optional[bool] = ...) -> None: ...

class TarefaRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TarefaResponse(_message.Message):
    __slots__ = ("tarefa",)
    TAREFA_FIELD_NUMBER: _ClassVar[int]
    tarefa: Tarefa
    def __init__(self, tarefa: _Optional[_Union[Tarefa, _Mapping]] = ...) -> None: ...

class ListTarefasResponse(_message.Message):
    __slots__ = ("tarefas",)
    TAREFAS_FIELD_NUMBER: _ClassVar[int]
    tarefas: _containers.RepeatedCompositeFieldContainer[Tarefa]
    def __init__(self, tarefas: _Optional[_Iterable[_Union[Tarefa, _Mapping]]] = ...) -> None: ...

class UpdateTarefaRequest(_message.Message):
    __slots__ = ("id", "title", "descricao", "completed")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRICAO_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    descricao: str
    completed: bool
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., descricao: _Optional[str] = ..., completed: _Optional[bool] = ...) -> None: ...

class DeleteTarefaResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: _Optional[bool] = ...) -> None: ...
