import pytest
from src.dominio.modelos import Mesa, Restaurante, Capacidade, Horario, JanelaTempo

class TestMesa:
    def test_criacao(self):
        capacidade = Capacidade(lugares=4)
        mesa = Mesa(id="mesa-1", numero=1, capacidade=capacidade)
        
        assert mesa.id == "mesa-1"
        assert mesa.numero == 1
        assert mesa.capacidade == capacidade
        assert mesa.ativa is True
    
    def test_pode_acomodar(self):
        mesa = Mesa(
            id="mesa-1", 
            numero=1, 
            capacidade=Capacidade(lugares=4)
        )
        
        assert mesa.pode_acomodar(3)
        assert mesa.pode_acomodar(4)
        assert not mesa.pode_acomodar(5)  # Excede capacidade
        
        # Mesa inativa
        mesa.ativa = False
        assert not mesa.pode_acomodar(2)

class TestRestaurante:
    @pytest.fixture
    def restaurante(self):
        return Restaurante(
            id="rest-1",
            nome="Teste",
            horarios_funcionamento={
                "monday": [
                    JanelaTempo(Horario(18, 0), Horario(23, 0))
                ]
            }
        )
    
    def test_esta_aberto(self, restaurante):
        from datetime import date
        
        # Segunda-feira (monday)
        data_segunda = date(2024, 1, 1)  # 1/1/2024 é segunda
        
        assert restaurante.esta_aberto(data_segunda, Horario(19, 30))
        assert restaurante.esta_aberto(data_segunda, Horario(18, 0))  # Início
        assert not restaurante.esta_aberto(data_segunda, Horario(17, 59))  # Antes
        assert not restaurante.esta_aberto(data_segunda, Horario(23, 0))  # Fim exclusivo
    
    def test_nao_funciona_dia(self, restaurante):
        from datetime import date
        
        # Terça-feira (não configurada)
        data_terca = date(2024, 1, 2)  # 2/1/2024 é terça
        
        assert not restaurante.esta_aberto(data_terca, Horario(19, 30))