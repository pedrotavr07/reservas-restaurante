from ..modelos.value_objects import Horario, JanelaTempo

def validar_janela_reserva(horario: Horario) -> bool:
    """Reservas só entre 18h e 23h"""
    return 18 <= horario.hora < 23

def calcular_duracao_turno(janela: JanelaTempo) -> int:
    """Quanto tempo (em horas) dura um turno?"""
    return janela.fim.hora - janela.inicio.hora