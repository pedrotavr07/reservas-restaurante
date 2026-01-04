from src.app.dtos import CancelarReservaComando, Resultado

class CasoDeUsoCancelarReserva:
    def __init__(self, repositorio_reservas):
        self.repositorio_reservas = repositorio_reservas
    
    def executar(self, comando: CancelarReservaComando) -> Resultado:
        try:
            reserva = self.repositorio_reservas.buscar_por_id(comando.reserva_id)
            
            if not reserva:
                return Resultado.erro("Reserva não encontrada")
            
            if reserva.cliente_id != comando.cliente_id:
                return Resultado.erro("Esta reserva não pertence a você")
            
            reserva.cancelar()
            
            return Resultado.sucesso({"mensagem": "Reserva cancelada com sucesso"})
            
        except Exception as e:
            return Resultado.erro(f"Erro ao cancelar reserva: {e}")