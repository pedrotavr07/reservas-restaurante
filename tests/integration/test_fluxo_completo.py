"""
Testes de integração - Fluxos completos do sistema
"""
import pytest
from datetime import date
from src.app.container import Container
from src.dominio.modelos import Horario

class TestFluxoCompleto:
    @pytest.fixture
    def container(self):
        return Container()
    
    @pytest.fixture
    def fachada(self, container):
        return container.fachada()
    
    def test_fluxo_reserva_cancelamento(self, fachada):
        # 1. Realizar reserva
        resultado_reserva = fachada.realizar_reserva(
            data=date(2024, 12, 25),
            horario="19:30",
            numero_pessoas=3,
            cliente_id="cliente-teste"
        )
        
        assert resultado_reserva.sucesso is True
        reserva_id = resultado_reserva.dados.id
        
        # 2. Consultar reservas do cliente
        resultado_consultas = fachada.consultar_reservas("cliente-teste")
        assert resultado_consultas.sucesso is True
        assert len(resultado_consultas.dados) == 1
        assert resultado_consultas.dados[0].id == reserva_id
        
        # 3. Cancelar reserva
        resultado_cancelamento = fachada.cancelar_reserva(
            reserva_id=reserva_id,
            cliente_id="cliente-teste"
        )
        
        assert resultado_cancelamento.sucesso is True
        
        # 4. Verificar que reserva foi cancelada
        reservas_final = fachada.consultar_reservas("cliente-teste")
        assert reservas_final.dados[0].status == "CANCELADA"
    
    def test_reservas_conflitantes(self, fachada):
        # Primeira reserva
        resultado1 = fachada.realizar_reserva(
            data=date(2024, 12, 25),
            horario="19:30",
            numero_pessoas=2,
            cliente_id="cliente-1"
        )
        
        assert resultado1.sucesso is True
        
        # Segunda reserva no mesmo horário (deve alocar mesa diferente)
        resultado2 = fachada.realizar_reserva(
            data=date(2024, 12, 25),
            horario="19:30",
            numero_pessoas=2,
            cliente_id="cliente-2"
        )
        
        assert resultado2.sucesso is True
        
        # Verificar que as reservas têm mesas diferentes
        assert resultado1.dados.mesa_numero != resultado2.dados.mesa_numero
    
    def test_capacidade_insuficiente(self, fachada):
        # Tentar reserva para 10 pessoas (a maior mesa tem 8 lugares)
        resultado = fachada.realizar_reserva(
            data=date(2024, 12, 25),
            horario="19:30",
            numero_pessoas=10,
            cliente_id="cliente-grande"
        )
        
        assert resultado.sucesso is False
        assert "disponível" in resultado.erro.lower()