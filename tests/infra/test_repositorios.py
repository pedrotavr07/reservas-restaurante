import pytest
from datetime import date
from src.dominio.modelos import Reserva, Mesa, Capacidade, Horario
from src.infra.repositorios.reservas_memoria import RepositorioReservasMemoria
from src.infra.repositorios.mesas_memoria import RepositorioMesasMemoria

class TestRepositorioReservasMemoria:
    @pytest.fixture
    def repositorio(self):
        return RepositorioReservasMemoria()
    
    @pytest.fixture
    def reserva_teste(self):
        mesa = Mesa(
            id="mesa-1",
            numero=1,
            capacidade=Capacidade(lugares=4)
        )
        return Reserva(
            id="res-1",
            data_reserva=date(2024, 12, 25),
            horario=Horario(19, 30),
            numero_pessoas=3,
            cliente_id="cliente-1",
            mesa=mesa
        )
    
    def test_salvar_buscar_por_id(self, repositorio, reserva_teste):
        repositorio.salvar(reserva_teste)
        
        encontrada = repositorio.buscar_por_id("res-1")
        assert encontrada is not None
        assert encontrada.id == "res-1"
        assert encontrada.cliente_id == "cliente-1"
    
    def test_salvar_gera_id_se_vazio(self, repositorio):
        mesa = Mesa(id="mesa-1", numero=1, capacidade=Capacidade(lugares=4))
        reserva = Reserva(
            id=None,  # Sem ID
            data_reserva=date(2024, 12, 25),
            horario=Horario(19, 30),
            numero_pessoas=3,
            cliente_id="cliente-1",
            mesa=mesa
        )
        
        repositorio.salvar(reserva)
        assert reserva.id is not None
        assert reserva.id.startswith("RES-")
    
    def test_buscar_por_data(self, repositorio, reserva_teste):
        repositorio.salvar(reserva_teste)
        
        # Reserva na data correta
        reservas_data = repositorio.buscar_por_data(date(2024, 12, 25))
        assert len(reservas_data) == 1
        assert reservas_data[0].id == "res-1"
        
        # Data sem reservas
        reservas_outra_data = repositorio.buscar_por_data(date(2024, 12, 26))
        assert len(reservas_outra_data) == 0
    
    def test_buscar_por_cliente(self, repositorio, reserva_teste):
        repositorio.salvar(reserva_teste)
        
        reservas_cliente = repositorio.buscar_por_cliente("cliente-1")
        assert len(reservas_cliente) == 1
        assert reservas_cliente[0].id == "res-1"
        
        reservas_outro_cliente = repositorio.buscar_por_cliente("cliente-2")
        assert len(reservas_outro_cliente) == 0

class TestRepositorioMesasMemoria:
    @pytest.fixture
    def repositorio(self):
        return RepositorioMesasMemoria()
    
    def test_listar_todas(self, repositorio):
        mesas = repositorio.listar_todas()
        assert len(mesas) == 4  # Tem 4 mesas no repositório padrão
        
        # Verifica se são instâncias de Mesa
        for mesa in mesas:
            assert isinstance(mesa, Mesa)
    
    def test_buscar_por_id(self, repositorio):
        mesa = repositorio.buscar_por_id("mesa-2")
        assert mesa is not None
        assert mesa.id == "mesa-2"
        assert mesa.numero == 2
        assert mesa.capacidade.lugares == 4
        
        mesa_inexistente = repositorio.buscar_por_id("mesa-99")
        assert mesa_inexistente is None
    
    def test_buscar_por_capacidade_minima(self, repositorio):
        # Mesas com capacidade mínima de 4 lugares
        mesas = repositorio.buscar_por_capacidade_minima(4)
        
        # Deve retornar 3 mesas (4, 6 e 8 lugares)
        assert len(mesas) == 3
        capacidades = [m.capacidade.lugares for m in mesas]
        assert 4 in capacidades
        assert 6 in capacidades
        assert 8 in capacidades
        
        # Mesas com capacidade mínima de 7 lugares
        mesas = repositorio.buscar_por_capacidade_minima(7)
        assert len(mesas) == 1  # Apenas mesa de 8 lugares
        assert mesas[0].capacidade.lugares == 8