import smtplib
from email.message import EmailMessage

SENDER_EMAIL = "unidraft2026@gmail.com"
SENDER_PASSWORD = "nvsi jkyv kgaz ohue"

def send_registration_email(treinador_email, atleta_email, seletiva):
    """Envia e-mail avisando o treinador sobre nova inscrição."""
    if not treinador_email:
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Nova inscrição na sua seletiva (ID {seletiva.get('id')})"
    msg["From"] = SENDER_EMAIL
    msg["To"] = treinador_email

    corpo = (
        f"Olá,\n\nO atleta {atleta_email} inscreveu-se na sua seletiva.\n\n"
        f"Detalhes:\nID: {seletiva.get('id')}\nEsporte: {seletiva.get('esporte')}\n"
        f"Data: {seletiva.get('data')}\nLimite: {seletiva.get('limite')}\n"
        f"Total de inscritos agora: {len(seletiva.get('inscritos', []))}\n\n"
        "Atenciosamente,\nUnidraft"
    )

    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False


def send_cancellation_email(treinador_email, atleta_email, seletiva):
    if not treinador_email:
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Cancelamento de inscrição na sua seletiva (ID {seletiva.get('id')})"
    msg["From"] = SENDER_EMAIL
    msg["To"] = treinador_email

    corpo = (
        f"Olá,\n\nO atleta {atleta_email} cancelou sua inscrição na sua seletiva.\n\n"
        f"Detalhes:\nID: {seletiva.get('id')}\nEsporte: {seletiva.get('esporte')}\n"
        f"Data: {seletiva.get('data')}\n"
        f"Total de inscritos agora: {len(seletiva.get('inscritos', []))}\n\n"
        "Atenciosamente,\nUnidraft"
    )

    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False


def send_seletiva_canceled_email(treinadores_email, seletiva):
    
    if not treinadores_email or not isinstance(treinadores_email, list):
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Seletiva cancelada (ID {seletiva.get('id')})"
    msg["From"] = SENDER_EMAIL

    corpo = (
        f"Olá,\n\nA seletiva foi cancelada.\n\n"
        f"Detalhes:\nID: {seletiva.get('id')}\nEsporte: {seletiva.get('esporte')}\n"
        f"Data: {seletiva.get('data')}\n"
        f"Inscritos: {len(seletiva.get('inscritos', []))}\n\n"
        "Atenciosamente,\nUnidraft"
    )

    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            for email in treinadores_email:
                msg["To"] = email
                smtp.send_message(msg)
        return True
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False
