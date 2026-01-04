from .dtos.comandos import RealizarReservaComando, CancelarReservaComando
from .dtos.respostas import Resultado

class FachadaReservas:
    def __init__(
        self,
        caso_realizar_reserva,
        caso_cancelar_reserva
    ):
        self.caso_realizar_reserva = caso_realizar_reserva
        self.caso_cancelar_reserva = caso_cancelar_reserva
    
    def realizar_reserva(self, data, horario, numero_pessoas, cliente_id) -> Resultado:
        comando = RealizarReservaComando(
            data=data,
            horario=horario,
            numero_pessoas=numero_pessoas,
            cliente_id=cliente_id
        )
        return self.caso_realizar_reserva.executar(comando)
    
    def cancelar_reserva(self, reserva_id, cliente_id) -> Resultado:
        comando = CancelarReservaComando(
            reserva_id=reserva_id,
            cliente_id=cliente_id
        )
        return self.caso_cancelar_reserva.executar(comando)
    
    def consultar_reservas(self, cliente_id) -> Resultado:
        # Implementação simplificada
        from src.infra.repositorios.reservas_memoria import RepositorioReservasMemoria
        repositorio = RepositorioReservasMemoria()
        reservas = repositorio.buscar_por_cliente(cliente_id)
        return Resultado.sucesso(reservas)
    
    def consultar_disponibilidade(self, data, horario, numero_pessoas) -> Resultado:
        # Implementação simplificada
        # Em uma versão completa, criaria um caso de uso específico
        return Resultado.sucesso({"mensagem": "Funcionalidade em desenvolvimento"})