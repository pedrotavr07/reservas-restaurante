def validar_capacidade_minima(lugares: int) -> bool:
    """Restaurante exige no mínimo 1 pessoa por reserva"""
    return lugares >= 1

def calcular_ocupacao_ideal(capacidade_total: int, ocupacao_atual: int) -> float:
    """Retorna a porcentagem de ocupação ideal (70%)"""
    return capacidade_total * 0.7