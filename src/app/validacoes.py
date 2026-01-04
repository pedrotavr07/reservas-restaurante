from datetime import date

def validar_data_futura(data: date) -> bool:
    return data >= date.today()

def validar_formato_horario(horario: str) -> bool:
    try:
        horas, minutos = horario.split(":")
        return 0 <= int(horas) <= 23 and 0 <= int(minutos) <= 59
    except:
        return False