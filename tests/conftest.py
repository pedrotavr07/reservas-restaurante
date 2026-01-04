"""
Configuração global do pytest para todos os testes
"""
import sys
import os
from datetime import datetime, date
import pytest

# Adiciona o src ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Fixtures globais
@pytest.fixture
def hoje():
    return date.today()

@pytest.fixture
def amanha(hoje):
    from datetime import timedelta
    return hoje + timedelta(days=1)

@pytest.fixture
def horario_valido():
    from src.dominio.modelos import Horario
    return Horario(19, 30)

@pytest.fixture
def capacidade_4_lugares():
    from src.dominio.modelos import Capacidade
    return Capacidade(lugares=4)

@pytest.fixture
def mesa_4_lugares(capacidade_4_lugares):
    from src.dominio.modelos import Mesa
    return Mesa(id="mesa-1", numero=1, capacidade=capacidade_4_lugares)

@pytest.fixture
def restaurante_padrao():
    from src.dominio.modelos import Restaurante, JanelaTempo, Horario
    return Restaurante(
        id="rest-1",
        nome="Restaurante Teste",
        horarios_funcionamento={
            "monday": [JanelaTempo(Horario(18, 0), Horario(23, 0))],
            "tuesday": [JanelaTempo(Horario(18, 0), Horario(23, 0))],
            "wednesday": [JanelaTempo(Horario(18, 0), Horario(23, 0))],
            "thursday": [JanelaTempo(Horario(18, 0), Horario(23, 0))],
            "friday": [JanelaTempo(Horario(18, 0), Horario(23, 0))],
            "saturday": [JanelaTempo(Horario(18, 0), Horario(23, 0))],
            "sunday": [JanelaTempo(Horario(18, 0), Horario(23, 0))],
        }
    )