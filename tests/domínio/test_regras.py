from src.dominio.regras.capacidade import (
    validar_capacidade_minima, 
    validar_capacidade_maxima
)

def test_validar_capacidade_minima():
    assert validar_capacidade_minima(1) is True
    assert validar_capacidade_minima(5) is True
    assert validar_capacidade_minima(0) is False
    assert validar_capacidade_minima(-1) is False

def test_validar_capacidade_maxima():
    # Padrão: máximo 20 pessoas
    assert validar_capacidade_maxima(15) is True
    assert validar_capacidade_maxima(20) is True
    assert validar_capacidade_maxima(21) is False
    
    # Com limite customizado
    assert validar_capacidade_maxima(5, maximo=10) is True
    assert validar_capacidade_maxima(15, maximo=10) is False