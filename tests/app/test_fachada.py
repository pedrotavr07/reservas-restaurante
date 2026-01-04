import pytest
from datetime import date
from unittest.mock import Mock
from src.app.fachada import FachadaReservas
from src.app.dtos.respostas import Resultado

class TestFachadaReservas:
    @pytest.fixture
    def casos_de_uso(self):
        return {
            'caso_realizar_reserva': Mock(),
            'caso_cancelar_reserva': Mock()
        }
    
    @pytest.fixture
    def fachada(self, casos_de_uso):
        return FachadaReservas(
            caso_realizar_reserva=casos_de_uso['caso_realizar_reserva'],
            caso_cancelar_reserva=casos_de_uso['caso_cancelar_reserva']
        )
    
    def test_realizar_reserva(self, fachada, casos_de_uso):
        # Configurar mock
        resultado_mock = Resultado.sucesso({"id": "res-1"})
        casos_de_uso['caso_realizar_reserva'].executar.return_value = resultado_mock
        
        # Chamar fachada
        resultado = fachada.realizar_reserva(
            data=date(2024, 12, 25),
            horario="19:30",
            numero_pessoas=3,
            cliente_id="cliente-1"
        )
        
        # Verificar
        assert resultado == resultado_mock
        casos_de_uso['caso_realizar_reserva'].executar.assert_called_once()
    
    def test_cancelar_reserva(self, fachada, casos_de_uso):
        resultado_mock = Resultado.sucesso({"mensagem": "Cancelada"})
        casos_de_uso['caso_cancelar_reserva'].executar.return_value = resultado_mock
        
        resultado = fachada.cancelar_reserva("res-1", "cliente-1")
        
        assert resultado == resultado_mock
        casos_de_uso['caso_cancelar_reserva'].executar.assert_called_once()