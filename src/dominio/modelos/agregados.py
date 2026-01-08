from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Optional
from .value_objects import Horario
from .entidades import Mesa
from .eventos import ReservaRealizada

# Regra de Negócio: Duração padrão de cada reserva
DURACAO_RESERVA_HORAS = 2

@dataclass
class Reserva:
    """Agregado Raiz"""
    id: str
    data_reserva: date
    horario: Horario
    numero_pessoas: int
    cliente_id: str
    mesa: Mesa
    status: str = "CONFIRMADA"
    criada_em: datetime = None
    _eventos: list = None
    
    def __post_init__(self):
        if self.criada_em is None:
            self.criada_em = datetime.now()
        if self._eventos is None:
            self._eventos = []
        
        self._validar()
        self._registrar_evento_criacao()
    

    def _validar(self):
        # Regra 1: Validação de data (Sua contribuição)
        if self.data_reserva < date.today():
            raise ValueError("Não é possível fazer reservas para datas passadas")
            
        if self.numero_pessoas <= 0:
            raise ValueError("Número de pessoas inválido")
            
        if not self.mesa.pode_acomodar(self.numero_pessoas):
            raise ValueError(f"Mesa não suporta {self.numero_pessoas} pessoas")
    
    def _registrar_evento_criacao(self):
        evento = ReservaRealizada(
            reserva_id=self.id,
            data_reserva=self.data_reserva,
            horario=self.horario,
            numero_pessoas=self.numero_pessoas,
            cliente_id=self.cliente_id,
            mesa_id=self.mesa.id
        )
        self._eventos.append(evento)
    
    @property
    def eventos(self):
        return list(self._eventos)
    
    def limpar_eventos(self):
        self._eventos.clear()

    def horario_fim_estimado(self) -> datetime:
        inicio = datetime.combine(self.data_reserva, 
                                 time(self.horario.hora, self.horario.minuto))
        return inicio + timedelta(hours=DURACAO_RESERVA_HORAS)
    
    def conflita_com(self, outra: 'Reserva') -> bool:
        if self.mesa.id != outra.mesa.id:
            return False
        if self.data_reserva != outra.data_reserva:
            return False
        
        inicio_self = self.horario_fim_estimado() - timedelta(hours=DURACAO_RESERVA_HORAS)
        fim_self = self.horario_fim_estimado()
        
        inicio_outra = outra.horario_fim_estimado() - timedelta(hours=DURACAO_RESERVA_HORAS)
        fim_outra = outra.horario_fim_estimado()
        
        return not (fim_self <= inicio_outra or fim_outra <= inicio_self)
    
    
    def cancelar(self):
        self.status = "CANCELADA"
        # Poderia adicionar evento ReservaCancelada