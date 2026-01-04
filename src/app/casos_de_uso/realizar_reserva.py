from datetime import datetime
from src.app.dtos import RealizarReservaComando, Resultado, ReservaDTO
from src.dominio.modelos import Reserva, Horario
from src.dominio.servicos import ServicoAlocacaoMesas
from src.dominio.regras import validar_capacidade_minima, validar_capacidade_maxima

class CasoDeUsoRealizarReserva:
    def __init__(
        self,
        repositorio_reservas,
        repositorio_mesas,
        repositorio_restaurantes,
        publicador_eventos
    ):
        self.repositorio_reservas = repositorio_reservas
        self.repositorio_mesas = repositorio_mesas
        self.repositorio_restaurantes = repositorio_restaurantes
        self.publicador_eventos = publicador_eventos
    
    def executar(self, comando: RealizarReservaComando) -> Resultado:
        try:
            # 1. Validações básicas
            horario = Horario.from_string(comando.horario)
            
            if not validar_capacidade_minima(comando.numero_pessoas):
                return Resultado.erro("Número de pessoas inválido")
            
            if not validar_capacidade_maxima(comando.numero_pessoas):
                return Resultado.erro("Número máximo de pessoas excedido")
            
            # 2. Verificar se restaurante está aberto
            restaurante = self.repositorio_restaurantes.buscar_principal()
            if not restaurante.esta_aberto(comando.data, horario):
                return Resultado.erro("Restaurante fechado neste horário")
            
            # 3. Buscar dados
            mesas = self.repositorio_mesas.listar_todas()
            reservas_existentes = self.repositorio_reservas.buscar_por_data(comando.data)
            
            # 4. Encontrar mesa (serviço de domínio)
            mesa = ServicoAlocacaoMesas.encontrar_mesa_otima(
                mesas, reservas_existentes,
                comando.data, horario, comando.numero_pessoas
            )
            
            if not mesa:
                return Resultado.erro("Nenhuma mesa disponível para este horário")
            
            # 5. Criar reserva (domínio)
            reserva = Reserva(
                id=self._gerar_id(),
                data_reserva=comando.data,
                horario=horario,
                numero_pessoas=comando.numero_pessoas,
                cliente_id=comando.cliente_id,
                mesa=mesa
            )
            
            # 6. Persistir
            self.repositorio_reservas.salvar(reserva)
            
            # 7. Publicar eventos
            for evento in reserva.eventos:
                self.publicador_eventos.publicar(evento)
            reserva.limpar_eventos()
            
            # 8. Retornar DTO
            dto = ReservaDTO(
                id=reserva.id,
                data=reserva.data_reserva.isoformat(),
                horario=str(reserva.horario),
                numero_pessoas=reserva.numero_pessoas,
                mesa_numero=reserva.mesa.numero,
                status=reserva.status,
                criada_em=reserva.criada_em
            )
            
            return Resultado.sucesso(dto)
            
        except ValueError as e:
            return Resultado.erro(str(e))
        except Exception as e:
            return Resultado.erro(f"Erro inesperado: {e}")
    
    def _gerar_id(self) -> str:
        return f"res-{datetime.now().strftime('%Y%m%d%H%M%S')}"