def deve_usar_mesa_menor_possivel(numero_pessoas: int, capacidade_mesa: int) -> bool:
    """Política: usar a menor mesa que acomode o grupo"""
    return capacidade_mesa >= numero_pessoas

def pode_dividir_mesa_grande(numero_pessoas: int, capacidade_mesa: int) -> bool:
    """Permitir dividir uma mesa grande para grupos menores?"""
    return capacidade_mesa >= numero_pessoas * 2  # Exemplo: mesa de 8 para 4 pessoas