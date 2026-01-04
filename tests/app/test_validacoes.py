from datetime import date
from src.app.validacoes import validar_data_futura, validar_formato_horario

def test_validar_data_futura():
    hoje = date.today()
    amanha = date(hoje.year, hoje.month, hoje.day + 1)
    ontem = date(hoje.year, hoje.month, hoje.day - 1)
    
    assert validar_data_futura(hoje) is True  # Hoje é válido
    assert validar_data_futura(amanha) is True
    assert validar_data_futura(ontem) is False

def test_validar_formato_horario():
    assert validar_formato_horario("08:30") is True
    assert validar_formato_horario("19:45") is True
    assert validar_formato_horario("23:59") is True
    assert validar_formato_horario("00:00") is True
    
    assert validar_formato_horario("24:00") is False  # Hora inválida
    assert validar_formato_horario("12:60") is False  # Minuto inválido
    assert validar_formato_horario("12.30") is False  # Formato errado
    assert validar_formato_horario("") is False
    assert validar_formato_horario("12345") is False