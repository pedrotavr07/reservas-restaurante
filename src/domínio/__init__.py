"""
Pacote do domínio - contém toda a lógica de negócio pura
"""
from .modelos.value_objects import Horario, Capacidade, JanelaTempo
from .modelos.entidades import Mesa, Restaurante
from .modelos.agregados import Reserva
from .modelos.eventos import ReservaRealizada
from .servicos.alocacao_mesas import ServicoAlocacaoMesas

__all__ = [
    'Horario',
    'Capacidade',
    'JanelaTempo',
    'Mesa',
    'Restaurante',
    'Reserva',
    'ReservaRealizada',
    'ServicoAlocacaoMesas',
]