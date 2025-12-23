from dataclasses import dataclass
from datetime import time
from typing import Self

@dataclass(frozen=True)
class Horario:
    hora: int  # 0-23
    minuto: int  # 0-59
    
    def __post_init__(self):
        if not (0 <= self.hora <= 23):
            raise ValueError("Hora inválida")
        if not (0 <= self.minuto <= 59):
            raise ValueError("Minuto inválido")
    
    def __str__(self):
        return f"{self.hora:02d}:{self.minuto:02d}"
    
    @classmethod
    def from_string(cls, horario_str: str) -> Self:
        hora, minuto = map(int, horario_str.split(':'))
        return cls(hora, minuto)

@dataclass(frozen=True)
class JanelaTempo:
    inicio: Horario
    fim: Horario
    
    def __post_init__(self):
        if self.fim <= self.inicio:
            raise ValueError("Fim deve ser depois do início")
    
    def contem(self, horario: Horario) -> bool:
        return self.inicio <= horario < self.fim

@dataclass(frozen=True)
class Capacidade:
    lugares: int
    
    def __post_init__(self):
        if self.lugares <= 0:
            raise ValueError("Capacidade deve ser positiva")
    
    def suporta(self, numero_pessoas: int) -> bool:
        return numero_pessoas <= self.lugares