import smtplib
from email.mime.text import MIMEText

class ServicoEmailSMTP:
    """Envia emails REAIS via SMTP"""
    
    def __init__(self, host, porta, usuario, senha):
        self.host = host
        self.porta = porta
        self.usuario = usuario
        self.senha = senha
    
    def enviar_confirmacao_reserva(self, email_cliente, reserva):
        """IMPLEMENTAÇÃO REAL do envio de email"""
        mensagem = MIMEText(f"Sua reserva {reserva.id} foi confirmada!")
        mensagem["Subject"] = "Confirmação de Reserva"
        mensagem["From"] = self.usuario
        mensagem["To"] = email_cliente
        
        with smtplib.SMTP(self.host, self.porta) as servidor:
            servidor.starttls()
            servidor.login(self.usuario, self.senha)
            servidor.send_message(mensagem)