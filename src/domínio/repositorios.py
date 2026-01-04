from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import date
from .modelos import Reserva, Mesa, Restaurante

# INTERFACES - definidas no domínio, implementadas na infra

class RepositorioReservas(ABC):
    @abstractmethod
    def salvar(self, reserva: Reserva) -> None:
        pass
    
    @abstractmethod
    def buscar_por_id(self, reserva_id: str) -> Optional[Reserva]:
        pass
    
    @abstractmethod
    def buscar_por_data(self, data: date) -> List[Reserva]:
        pass
    
    @abstractmethod
    def buscar_por_cliente(self, cliente_id: str) -> List[Reserva]:
        pass

class RepositorioMesas(ABC):
    @abstractmethod
    def buscar_por_id(self, mesa_id: str) -> Optional[Mesa]:
        pass
    
    @abstractmethod
    def listar_todas(self) -> List[Mesa]:
        pass
    
    @abstractmethod
    def buscar_por_capacidade_minima(self, lugares: int) -> List[Mesa]:
        pass

class PublicadorEventos(ABC):
    @abstractmethod
    def publicar(self, evento) -> None:
        pass