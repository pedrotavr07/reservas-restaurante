"""
Interface de Linha de Comando - Sem emojis
"""
import sys
from datetime import datetime, date
from src.app.container import Container
from src.app.fachada import FachadaReservas
from src.app.dtos.respostas import Resultado

class CLI:
    def __init__(self, fachada: FachadaReservas):
        self.fachada = fachada
    
    def executar(self):
        print("=" * 50)
        print("SISTEMA DE RESERVAS - RESTAURANTE DDD")
        print("=" * 50)
        
        while True:
            self._exibir_menu_principal()
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self._realizar_reserva()
            elif opcao == "2":
                self._consultar_reservas()
            elif opcao == "3":
                self._cancelar_reserva()
            elif opcao == "4":
                self._consultar_disponibilidade()
            elif opcao == "0":
                print("\nAté logo!")
                sys.exit(0)
            else:
                print("\nOpção inválida!")
            
            input("\nPressione Enter para continuar...")
    
    def _exibir_menu_principal(self):
        print("\n" + "=" * 30)
        print("MENU PRINCIPAL")
        print("=" * 30)
        print("1. Nova Reserva")
        print("2. Minhas Reservas")
        print("3. Cancelar Reserva")
        print("4. Ver Disponibilidade")
        print("0. Sair")
    
    def _realizar_reserva(self):
        print("\n" + "=" * 30)
        print("NOVA RESERVA")
        print("=" * 30)
        
        data_str = input("Data (YYYY-MM-DD): ").strip()
        if not self._validar_data(data_str):
            print("ERRO: Data inválida!")
            return
        
        horario_str = input("Horário (HH:MM): ").strip()
        if not self._validar_horario(horario_str):
            print("ERRO: Horário inválido! Use formato HH:MM")
            return
        
        try:
            pessoas = int(input("Número de pessoas: ").strip())
            if pessoas <= 0:
                print("ERRO: Número de pessoas inválido!")
                return
        except ValueError:
            print("ERRO: Digite um número válido!")
            return
        
        cliente_id = input("Seu ID (email ou nome): ").strip()
        if not cliente_id:
            print("ERRO: ID do cliente é obrigatório!")
            return
        
        resultado = self.fachada.realizar_reserva(
            date.fromisoformat(data_str),
            horario_str,
            pessoas,
            cliente_id
        )
        
        self._exibir_resultado(resultado)
    
    def _consultar_reservas(self):
        print("\n" + "=" * 30)
        print("MINHAS RESERVAS")
        print("=" * 30)
        
        cliente_id = input("Seu ID: ").strip()
        if not cliente_id:
            print("ERRO: ID é obrigatório!")
            return
        
        resultado = self.fachada.consultar_reservas(cliente_id)
        
        if resultado.sucesso:
            reservas = resultado.dados
            if not reservas:
                print("\nNenhuma reserva encontrada")
            else:
                print(f"\nVocê tem {len(reservas)} reserva(s):")
                print("-" * 40)
                for reserva in reservas:
                    print(f"ID: {reserva.id}")
                    print(f"  Data: {reserva.data_reserva}")
                    print(f"  Horário: {reserva.horario}")
                    print(f"  Pessoas: {reserva.numero_pessoas}")
                    print(f"  Mesa: {reserva.mesa.numero}")
                    print(f"  Status: {reserva.status}")
                    print("-" * 20)
        else:
            print(f"\nERRO: {resultado.erro}")
    
    def _cancelar_reserva(self):
        print("\n" + "=" * 30)
        print("CANCELAR RESERVA")
        print("=" * 30)
        
        reserva_id = input("ID da reserva: ").strip()
        cliente_id = input("Seu ID (para confirmação): ").strip()
        
        if not reserva_id or not cliente_id:
            print("ERRO: Todos os campos são obrigatórios!")
            return
        
        resultado = self.fachada.cancelar_reserva(reserva_id, cliente_id)
        self._exibir_resultado(resultado)
    
    def _consultar_disponibilidade(self):
        print("\n" + "=" * 30)
        print("CONSULTAR DISPONIBILIDADE")
        print("=" * 30)
        
        data_str = input("Data (YYYY-MM-DD): ").strip()
        horario_str = input("Horário (HH:MM): ").strip()
        pessoas = input("Número de pessoas: ").strip()
        
        if not self._validar_data(data_str):
            print("ERRO: Data inválida!")
            return
        
        if not self._validar_horario(horario_str):
            print("ERRO: Horário inválido!")
            return
        
        try:
            pessoas_int = int(pessoas)
        except ValueError:
            print("ERRO: Número de pessoas inválido!")
            return
        
        # Implementação simplificada
        print("\nEsta funcionalidade está em desenvolvimento...")
    
    def _validar_data(self, data_str: str) -> bool:
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def _validar_horario(self, horario_str: str) -> bool:
        try:
            hora, minuto = map(int, horario_str.split(":"))
            return 0 <= hora <= 23 and 0 <= minuto <= 59
        except (ValueError, AttributeError):
            return False
    
    def _exibir_resultado(self, resultado: Resultado):
        if resultado.sucesso:
            print(f"\nSUCESSO: Operação realizada com sucesso!")
            if resultado.dados and hasattr(resultado.dados, 'id'):
                reserva = resultado.dados
                print(f"\nDetalhes da reserva:")
                print(f"   ID: {reserva.id}")
                print(f"   Data: {reserva.data}")
                print(f"   Horário: {reserva.horario}")
                print(f"   Pessoas: {reserva.numero_pessoas}")
                print(f"   Mesa: {reserva.mesa_numero}")
                print(f"   Status: {reserva.status}")
        else:
            print(f"\nERRO: {resultado.erro}")

def main():
    container = Container()
    fachada = container.fachada()
    ui = CLI(fachada)
    ui.executar()

if __name__ == "__main__":
    main()