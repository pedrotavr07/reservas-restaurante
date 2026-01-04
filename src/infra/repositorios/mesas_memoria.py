from typing import Dict, List, Optional
from src.dominio.repositorios import RepositorioMesas
from src.dominio.modelos import Mesa, Capacidade

class RepositorioMesasMemoria(RepositorioMesas):
    def __init__(self):
        self._mesas: Dict[str, Mesa] = {
            "mesa-1": Mesa(id="mesa-1", numero=1, capacidade=Capacidade(lugares=2)),
            "mesa-2": Mesa(id="mesa-2", numero=2, capacidade=Capacidade(lugares=4)),
            "mesa-3": Mesa(id="mesa-3", numero=3, capacidade=Capacidade(lugares=6)),
            "mesa-4": Mesa(id="mesa-4", numero=4, capacidade=Capacidade(lugares=8)),
        }
    
    def buscar_por_id(self, mesa_id: str) -> Optional[Mesa]:
        return self._mesas.get(mesa_id)
    
    def listar_todas(self) -> List[Mesa]:
        return list(self._mesas.values())
    
    def buscar_por_capacidade_minima(self, lugares: int) -> List[Mesa]:
        return [
            mesa for mesa in self._mesas.values()
            if mesa.capacidade.lugares >= lugares
        ]