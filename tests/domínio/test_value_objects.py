import pytest
from datetime import date
from src.dominio.modelos import Horario, JanelaTempo, Capacidade

class TestHorario:
    def test_criacao_valida(self):
        horario = Horario(19, 30)
        assert horario.hora == 19
        assert horario.minuto == 30
        assert str(horario) == "19:30"
    
    def test_criacao_invalida(self):
        with pytest.raises(ValueError):
            Horario(25, 0)  # Hora inválida
        
        with pytest.raises(ValueError):
            Horario(12, 60)  # Minuto inválido
    
    def test_from_string(self):
        horario = Horario.from_string("08:15")
        assert horario.hora == 8
        assert horario.minuto == 15
    
    def test_comparacao(self):
        h1 = Horario(10, 0)
        h2 = Horario(10, 30)
        h3 = Horario(10, 0)
        
        assert h1 < h2
        assert h2 > h1
        assert h1 == h3
        assert h1 <= h3

class TestJanelaTempo:
    def test_criacao_valida(self):
        inicio = Horario(18, 0)
        fim = Horario(23, 0)
        janela = JanelaTempo(inicio, fim)
        
        assert janela.inicio == inicio
        assert janela.fim == fim
    
    def test_criacao_invalida(self):
        inicio = Horario(20, 0)
        fim = Horario(19, 0)  # Fim antes do início
        
        with pytest.raises(ValueError):
            JanelaTempo(inicio, fim)
    
    def test_contem(self):
        janela = JanelaTempo(Horario(18, 0), Horario(23, 0))
        
        assert janela.contem(Horario(19, 30))
        assert janela.contem(Horario(18, 0))
        assert not janela.contem(Horario(17, 59))
        assert not janela.contem(Horario(23, 0))  # Fim é exclusivo
        assert not janela.contem(Horario(23, 1))

class TestCapacidade:
    def test_criacao_valida(self):
        capacidade = Capacidade(lugares=4)
        assert capacidade.lugares == 4
    
    def test_criacao_invalida(self):
        with pytest.raises(ValueError):
            Capacidade(lugares=0)
        
        with pytest.raises(ValueError):
            Capacidade(lugares=-1)
    
    def test_suporta(self):
        capacidade = Capacidade(lugares=4)
        
        assert capacidade.suporta(3)
        assert capacidade.suporta(4)
        assert not capacidade.suporta(5)