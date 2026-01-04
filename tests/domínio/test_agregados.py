import pytest
from datetime import date
from src.dominio.modelos import Reserva, Mesa, Capacidade, Horario

class TestReserva:
    @pytest.fixture
    def mesa_4_lugares(self):
        return Mesa(
            id="mesa-1",
            numero=1,
            capacidade=Capacidade(lugares=4)
        )
    
    def test_criacao_valida(self, mesa_4_lugares):
        reserva = Reserva(
            id="res-1",
            data_reserva=date(2024, 12, 25),
            horario=Horario(19, 30),
            numero_pessoas=3,
            cliente_id="cliente-1",
            mesa=mesa_4_lugares
        )
        
        assert reserva.id == "res-1"
        assert reserva.numero_pessoas == 3
        assert reserva.status == "CONFIRMADA"
        assert len(reserva.eventos) == 1  # Deve ter evento de criação
    
    def test_criacao_invalida_capacidade(self, mesa_4_lugares):
        with pytest.raises(ValueError, match="não suporta"):
            Reserva(
                id="res-1",
                data_reserva=date(2024, 12, 25),
                horario=Horario(19, 30),
                numero_pessoas=5,  # Mesa só suporta 4
                cliente_id="cliente-1",
                mesa=mesa_4_lugares
            )
    
    def test_criacao_invalida_pessoas(self, mesa_4_lugares):
        with pytest.raises(ValueError, match="inválido"):
            Reserva(
                id="res-1",
                data_reserva=date(2024, 12, 25),
                horario=Horario(19, 30),
                numero_pessoas=0,  # Número inválido
                cliente_id="cliente-1",
                mesa=mesa_4_lugares
            )
    
    def test_conflita_com(self, mesa_4_lugares):
        reserva1 = Reserva(
            id="res-1",
            data_reserva=date(2024, 12, 25),
            horario=Horario(19, 30),
            numero_pessoas=3,
            cliente_id="cliente-1",
            mesa=mesa_4_lugares
        )
        
        reserva2 = Reserva(
            id="res-2",
            data_reserva=date(2024, 12, 25),  # Mesma data
            horario=Horario(20, 0),  # Sobreposição (19:30-21:30 vs 20:00-22:00)
            numero_pessoas=2,
            cliente_id="cliente-2",
            mesa=mesa_4_lugares
        )
        
        reserva3 = Reserva(
            id="res-3",
            data_reserva=date(2024, 12, 26),  # Data diferente
            horario=Horario(19, 30),
            numero_pessoas=2,
            cliente_id="cliente-3",
            mesa=mesa_4_lugares
        )
        
        assert reserva1.conflita_com(reserva2)
        assert not reserva1.conflita_com(reserva3)
    
    def test_cancelar(self, mesa_4_lugares):
        reserva = Reserva(
            id="res-1",
            data_reserva=date(2024, 12, 25),
            horario=Horario(19, 30),
            numero_pessoas=3,
            cliente_id="cliente-1",
            mesa=mesa_4_lugares
        )
        
        assert reserva.status == "CONFIRMADA"
        reserva.cancelar()
        assert reserva.status == "CANCELADA"