from dataclasses import dataclass
from datetime import date, datetime
from .value_objects import Horario, JanelaTempo, Capacidade

@dataclass
class Mesa:
    id: str
    numero: int
    capacidade: Capacidade
    ativa: bool = True
    
    def pode_acomodar(self, numero_pessoas: int) -> bool:
        return self.ativa and self.capacidade.suporta(numero_pessoas)

@dataclass
class Restaurante:
    id: str
    nome: str
    horarios_funcionamento: dict[str, list[JanelaTempo]]  # dia -> lista de janelas
    
    def esta_aberto(self, data: date, horario: Horario) -> bool:
        dia_semana = data.strftime("%A").lower()
        if dia_semana not in self.horarios_funcionamento:
            return False
        
        return any(
            janela.contem(horario)
            for janela in self.horarios_funcionamento[dia_semana]
        )
    
@dataclass
class Cliente:
    id: str
    nome: str
    telefone: str