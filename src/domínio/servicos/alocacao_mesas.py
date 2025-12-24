from typing import Optional
from ..modelos import Mesa, Reserva, Horario
from datetime import date

class ServicoAlocacaoMesas:
    """Serviço de Domínio - Contém regras complexas de alocação"""
    
    @staticmethod
    def encontrar_mesa_otima(
        mesas: list[Mesa],
        reservas_existentes: list[Reserva],
        data: date,
        horario: Horario,
        numero_pessoas: int
    ) -> Optional[Mesa]:
        # 1. Filtrar mesas com capacidade adequada
        mesas_validas = [m for m in mesas if m.pode_acomodar(numero_pessoas)]
        
        # 2. Ordenar por eficiência (menor mesa disponível primeiro)
        mesas_validas.sort(key=lambda m: m.capacidade.lugares)
        
        # 3. Verificar disponibilidade
        for mesa in mesas_validas:
            if ServicoAlocacaoMesas._mesa_disponivel(
                mesa, reservas_existentes, data, horario
            ):
                return mesa
        
        return None
    
    @staticmethod
    def _mesa_disponivel(
        mesa: Mesa,
        reservas: list[Reserva],
        data: date,
        horario: Horario
    ) -> bool:
        """Verifica se mesa está livre no horário"""
        for reserva in reservas:
            if reserva.mesa.id == mesa.id and reserva.data_reserva == data:
                if reserva.conflita_com(Reserva(
                    id="temp",
                    data_reserva=data,
                    horario=horario,
                    numero_pessoas=1,
                    cliente_id="temp",
                    mesa=mesa
                )):
                    return False
        return True