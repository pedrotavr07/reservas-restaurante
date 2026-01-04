import pytest
from unittest.mock import Mock, patch
from io import StringIO
import sys
from src.ui.cli import CLI
from src.app.dtos.respostas import Resultado, ReservaDTO
from datetime import datetime

class TestCLI:
    @pytest.fixture
    def fachada_mock(self):
        return Mock()
    
    @pytest.fixture
    def cli(self, fachada_mock):
        return CLI(fachada_mock)
    
    def test_exibir_menu_principal(self, cli):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli._exibir_menu_principal()
            output = fake_out.getvalue()
            
            assert "MENU PRINCIPAL" in output
            assert "1. Nova Reserva" in output
            assert "2. Minhas Reservas" in output
            assert "3. Cancelar Reserva" in output
            assert "0. Sair" in output
    
    def test_validar_data_valida(self, cli):
        assert cli._validar_data("2024-12-25") is True
    
    def test_validar_data_invalida(self, cli):
        assert cli._validar_data("2024/12/25") is False  # Formato errado
        assert cli._validar_data("2024-13-01") is False  # Mês inválido
        assert cli._validar_data("2024-12-32") is False  # Dia inválido
        assert cli._validar_data("data") is False
    
    def test_validar_horario_valido(self, cli):
        assert cli._validar_horario("08:30") is True
        assert cli._validar_horario("19:45") is True
        assert cli._validar_horario("23:59") is True
    
    def test_validar_horario_invalido(self, cli):
        assert cli._validar_horario("24:00") is False
        assert cli._validar_horario("12:60") is False
        assert cli._validar_horario("12.30") is False
        assert cli._validar_horario("") is False
    
    def test_exibir_resultado_sucesso(self, cli):
        reserva_dto = ReservaDTO(
            id="res-1",
            data="2024-12-25",
            horario="19:30",
            numero_pessoas=3,
            mesa_numero=1,
            status="CONFIRMADA",
            criada_em=datetime.now()
        )
        
        resultado = Resultado.sucesso(reserva_dto)
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli._exibir_resultado(resultado)
            output = fake_out.getvalue()
            
            assert "SUCESSO" in output
            assert "res-1" in output
            assert "2024-12-25" in output
            assert "19:30" in output
    
    def test_exibir_resultado_erro(self, cli):
        resultado = Resultado.erro("Mesa não disponível")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli._exibir_resultado(resultado)
            output = fake_out.getvalue()
            
            assert "ERRO" in output
            assert "Mesa não disponível" in output
    
    @patch('builtins.input')
    def test_realizar_reserva_fluxo_valido(self, mock_input, cli, fachada_mock):
        # Simular entradas do usuário
        mock_input.side_effect = [
            "2024-12-25",  # Data
            "19:30",       # Horário
            "3",           # Número de pessoas
            "cliente-1"    # ID do cliente
        ]
        
        # Mock da fachada
        reserva_dto = ReservaDTO(
            id="res-1",
            data="2024-12-25",
            horario="19:30",
            numero_pessoas=3,
            mesa_numero=1,
            status="CONFIRMADA",
            criada_em=datetime.now()
        )
        fachada_mock.realizar_reserva.return_value = Resultado.sucesso(reserva_dto)
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli._realizar_reserva()
            output = fake_out.getvalue()
            
            assert "NOVA RESERVA" in output
            fachada_mock.realizar_reserva.assert_called_once_with(
                "2024-12-25", "19:30", 3, "cliente-1"
            )
    
    @patch('builtins.input')
    def test_realizar_reserva_data_invalida(self, mock_input, cli, fachada_mock):
        # Data inválida
        mock_input.side_effect = [
            "2024/12/25",  # Data inválida
        ]
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli._realizar_reserva()
            output = fake_out.getvalue()
            
            assert "ERRO" in output or "inválida" in output
            fachada_mock.realizar_reserva.assert_not_called()