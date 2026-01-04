class RepositorioReservasMemoria:
    """Implementação CONCRETA da interface RepositorioReservas"""
    
    def __init__(self):
        self._reservas = {}  # Dict em memória
        self._contador = 0
    
    def salvar(self, reserva):
        """Implementação REAL de como salvar"""
        if reserva.id is None:
            self._contador += 1
            reserva.id = f"RES-{self._contador}"
        
        self._reservas[reserva.id] = reserva
        return reserva
    
    def buscar_por_id(self, reserva_id):
        return self._reservas.get(reserva_id)
    
    def listar_por_data(self, data):
        return [
            r for r in self._reservas.values() 
            if r.data_reserva == data
        ]