from src.dominio.repositorios import RepositorioRestaurantes
from src.dominio.modelos import Restaurante, JanelaTempo, Horario

class RepositorioRestaurantesMemoria(RepositorioRestaurantes):
    def __init__(self):
        self._restaurante = Restaurante(
            id="rest-1",
            nome="Restaurante DDD",
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
    
    def buscar_principal(self) -> Restaurante:
        return self._restaurante