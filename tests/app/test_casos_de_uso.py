import pytest
from datetime import date
from unittest.mock import Mock, MagicMock
from src.app.casos_de_uso.realizar_reserva import CasoDeUsoRealizarReserva
from src.app.casos_de_uso.cancelar_reserva import CasoDeUsoCancelarReserva
from src.app.dtos.comandos import RealizarReservaComando, CancelarReservaComando
from src.dominio.modelos import Mesa, Capacidade, Horario

class TestCasoDeUsoRealizarReserva:
    @pytest.fixture
    def dependencias(self):
        return {
            'repositorio_reservas': Mock(),
            'repositorio_mesas': Mock(),
            'repositorio_restaurantes': Mock(),
            'publicador_eventos': Mock()
        }
    
    @pytest.fixture
    def caso_de_uso(self, dependencias):
        return CasoDeUsoRealizarReserva(**dependencias)
    
    @pytest.fixture
    def comando_valido(self):
        return RealizarReservaComando(
            data=date(2024, 12, 25),
            horario="19:30",
            numero_pessoas=3,
            cliente_id="cliente-1"
        )
    
    def test_executar_sucesso(self, caso_de_uso, comando_valido, dependencias):
        # Configurar mocks
        restaurante_mock = Mock()
        restaurante_mock.esta_aberto.return_value = True
        dependencias['repositorio_restaurantes'].buscar_principal.return_value = restaurante_mock
        
        mesa = Mesa(id="mesa-1", numero=1, capacidade=Capacidade(lugares=4))
        dependencias['repositorio_mesas'].listar_todas.return_value = [mesa]
        dependencias['repositorio_reservas'].buscar_por_data.return_value = []
        
        # Executar
        resultado = caso_de_uso.executar(comando_valido)
        
        # Verificar
        assert resultado.sucesso is True
        assert resultado.dados is not None
        assert resultado.dados.numero_pessoas == 3
        
        # Verificar chamadas
        dependencias['repositorio_reservas'].salvar.assert_called_once()
        dependencias['publicador_eventos'].publicar.assert_called_once()
    
    def test_executar_restaurante_fechado(self, caso_de_uso, comando_valido, dependencias):
        restaurante_mock = Mock()
        restaurante_mock.esta_aberto.return_value = False
        dependencias['repositorio_restaurantes'].buscar_principal.return_value = restaurante_mock
        
        resultado = caso_de_uso.executar(comando_valido)
        
        assert resultado.sucesso is False
        assert "fechado" in resultado.erro.lower()
    
    def test_executar_sem_mesa_disponivel(self, caso_de_uso, comando_valido, dependencias):
        restaurante_mock = Mock()
        restaurante_mock.esta_aberto.return_value = True
        dependencias['repositorio_restaurantes'].buscar_principal.return_value = restaurante_mock
        
        # Mesa muito pequena
        mesa = Mesa(id="mesa-1", numero=1, capacidade=Capacidade(lugares=2))
        dependencias['repositorio_mesas'].listar_todas.return_value = [mesa]
        dependencias['repositorio_reservas'].buscar_por_data.return_value = []
        
        resultado = caso_de_uso.executar(comando_valido)
        
        assert resultado.sucesso is False
        assert "disponível" in resultado.erro.lower()

class TestCasoDeUsoCancelarReserva:
    @pytest.fixture
    def repositorio_reservas(self):
        return Mock()
    
    @pytest.fixture
    def caso_de_uso(self, repositorio_reservas):
        return CasoDeUsoCancelarReserva(repositorio_reservas)
    
    @pytest.fixture
    def comando_valido(self):
        return CancelarReservaComando(
            reserva_id="res-1",
            cliente_id="cliente-1"
        )
    
    def test_executar_sucesso(self, caso_de_uso, comando_valido, repositorio_reservas):
        # Mock da reserva
        reserva_mock = Mock()
        reserva_mock.cliente_id = "cliente-1"
        reserva_mock.status = "CONFIRMADA"
        repositorio_reservas.buscar_por_id.return_value = reserva_mock
        
        resultado = caso_de_uso.executar(comando_valido)
        
        assert resultado.sucesso is True
        reserva_mock.cancelar.assert_called_once()
    
    def test_executar_reserva_nao_encontrada(self, caso_de_uso, comando_valido, repositorio_reservas):
        repositorio_reservas.buscar_por_id.return_value = None
        
        resultado = caso_de_uso.executar(comando_valido)
        
        assert resultado.sucesso is False
        assert "encontrada" in resultado.erro.lower()
    
    def test_executar_cliente_diferente(self, caso_de_uso, comando_valido, repositorio_reservas):
        reserva_mock = Mock()
        reserva_mock.cliente_id = "outro-cliente"  # Diferente do comando
        repositorio_reservas.buscar_por_id.return_value = reserva_mock
        
        resultado = caso_de_uso.executar(comando_valido)
        
        assert resultado.sucesso is False
        assert "não pertence" in resultado.erro.lower()