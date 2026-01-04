from dataclasses import dataclass
from datetime import date

@dataclass
class RealizarReservaComando:
    data: date
    horario: str
    numero_pessoas: int
    cliente_id: str

@dataclass
class CancelarReservaComando:
    reserva_id: str
    cliente_id: str