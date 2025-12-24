from dataclasses import dataclass
from datetime import datetime, date
from .value_objects import Horario

@dataclass
class ReservaRealizada:
    reserva_id: str
    data_reserva: date
    horario: Horario
    numero_pessoas: int
    cliente_id: str
    mesa_id: str
    ocorrido_em: datetime = None
    
    def __post_init__(self):
        if self.ocorrido_em is None:
            self.ocorrido_em = datetime.now()