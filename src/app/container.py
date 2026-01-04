from dependency_injector import containers, providers
from src.infra.repositorios import (
    RepositorioReservasMemoria,
    RepositorioMesasMemoria,
    RepositorioRestaurantesMemoria
)
from src.infra.eventos import PublicadorEventosConsole
from src.app.casos_de_uso import (
    CasoDeUsoRealizarReserva,
    CasoDeUsoCancelarReserva
)
from src.app.fachada import FachadaReservas

class Container(containers.DeclarativeContainer):
    # Configurações
    config = providers.Configuration()
    
    # Repositórios (Infra)
    repositorio_reservas = providers.Singleton(RepositorioReservasMemoria)
    repositorio_mesas = providers.Singleton(RepositorioMesasMemoria)
    repositorio_restaurantes = providers.Singleton(RepositorioRestaurantesMemoria)
    
    # Eventos (Infra)
    publicador_eventos = providers.Singleton(PublicadorEventosConsole)
    
    # Casos de Uso (App)
    caso_realizar_reserva = providers.Factory(
        CasoDeUsoRealizarReserva,
        repositorio_reservas=repositorio_reservas,
        repositorio_mesas=repositorio_mesas,
        repositorio_restaurantes=repositorio_restaurantes,
        publicador_eventos=publicador_eventos
    )
    
    caso_cancelar_reserva = providers.Factory(
        CasoDeUsoCancelarReserva,
        repositorio_reservas=repositorio_reservas
    )
    
    # Fachada (App)
    fachada = providers.Factory(
        FachadaReservas,
        caso_realizar_reserva=caso_realizar_reserva,
        caso_cancelar_reserva=caso_cancelar_reserva
    )