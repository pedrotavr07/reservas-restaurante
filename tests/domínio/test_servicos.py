import pytest
from datetime import date
from src.dominio.modelos import Mesa, Capacidade, Horario, Reserva
from src.dominio.servicos import ServicoAlocacaoMesas

class TestServicoAlocacaoMesas:
    @pytest.fixture
    def mesas(self):
        return [
            Mesa(id="mesa-2", numero=2, capacidade=Capacidade(lugares=2)),
            Mesa(id="mesa-4", numero=4, capacidade=Capacidade(lugares=4)),
            Mesa(id="mesa-6", numero=6, capacidade=Capacidade(lugares=6)),
        ]
    
    @pytest.fixture
    def reserva_existente(self):
        mesa = Mesa(id="mesa-4", numero=4, capacidade=Capacidade(lugares=4))
        return Reserva(
            id="res-1",
            data_reserva=date(2024, 12, 25),
            horario=Horario(19, 30),
            numero_pessoas=3,
            cliente_id="cliente-1",
            mesa=mesa
        )
    
    def test_encontrar_mesa_otima_sem_reservas(self, mesas):
        # Sem reservas existentes
        mesa = ServicoAlocacaoMesas.encontrar_mesa_otima(
            mesas=mesas,
            reservas_existentes=[],
            data=date(2024, 12, 25),
            horario=Horario(19, 30),
            numero_pessoas=3
        )
        
        # Deve retornar a menor mesa que cabe (mesa de 4 lugares)
        assert mesa is not None
        assert mesa.id == "mesa-4"
    
    def test_encontrar_mesa_otima_com_reservas(self, mesas, reserva_existente):
        # Com reserva existente na mesa-4 no mesmo horário
        mesa = ServicoAlocacaoMesas.encontrar_mesa_otima(
            mesas=mesas,
            reservas_existentes=[reserva_existente],
            data=date(2024, 12, 25),
            horario=Horario(19, 30),  # Mesmo horário → conflito
            numero_pessoas=3
        )
        
        # Deve pular a mesa-4 (ocupada) e ir para a mesa-6
        assert mesa is not None
        assert mesa.id == "mesa-6"
    
    def test_encontrar_mesa_otima_sem_mesa_disponivel(self, mesas):
        # Procurando mesa para 8 pessoas, mas a maior tem 6 lugares
        mesa = ServicoAlocacaoMesas.encontrar_mesa_otima(
            mesas=mesas,
            reservas_existentes=[],
            data=date(2024, 12, 25),
            horario=Horario(19, 30),
            numero_pessoas=8
        )
        
        assert mesa is None
    
    def test_mesa_disponivel(self, mesas, reserva_existente):
        # Teste do método auxiliar
        mesa_ocupada = mesas[1]  # mesa-4 (que tem reserva)
        mesa_livre = mesas[2]    # mesa-6
        
        assert not ServicoAlocacaoMesas._mesa_disponivel(
            mesa_ocupada, [reserva_existente], date(2024, 12, 25), Horario(19, 30)
        )
        
        assert ServicoAlocacaoMesas._mesa_disponivel(
            mesa_livre, [reserva_existente], date(2024, 12, 25), Horario(19, 30)
        )