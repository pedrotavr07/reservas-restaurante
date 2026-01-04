from typing import List
from src.dominio.repositorios import PublicadorEventos

class PublicadorEventosConsole(PublicadorEventos):
    def __init__(self):
        self.eventos_publicados: List = []
    
    def publicar(self, evento) -> None:
        self.eventos_publicados.append(evento)
        print(f"[EVENTO] {evento.__class__.__name__}: {evento}")