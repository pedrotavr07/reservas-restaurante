from dataclasses import dataclass
from typing import Optional, Any
from datetime import datetime

@dataclass
class Resultado:
    sucesso: bool
    dados: Optional[Any] = None
    erro: Optional[str] = None
    
    @classmethod
    def sucesso(cls, dados=None):
        return cls(sucesso=True, dados=dados)
    
    @classmethod
    def erro(cls, mensagem: str):
        return cls(sucesso=False, erro=mensagem)

@dataclass
class ReservaDTO:
    id: str
    data: str
    horario: str
    numero_pessoas: int
    mesa_numero: int
    status: str
    criada_em: datetime