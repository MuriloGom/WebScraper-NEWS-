import os
import smtplib

from dotenv import load_dotenv
from email.message import EmailMessage


load_dotenv()


def enviar_email(noticias):

    email_usuario = os.getenv("EMAIL_USER")
    email_senha = os.getenv("EMAIL_PASSWORD")
    email_destino = os.getenv("EMAIL_TO")

    mensagem = EmailMessage()

    mensagem["Subject"] = "Notícias de Hoje"
    mensagem["From"] = email_usuario
    mensagem["To"] = email_destino

    texto = "Olá!\n\n"
    texto += "Estas são as primeiras notícias encontradas no G1:\n\n"

    for i, noticia in enumerate(noticias, start=1):

        if isinstance(noticia, dict):
            titulo = noticia.get("titulo") or noticia.get("title") or "Sem título"
            link = noticia.get("link") or noticia.get("href") or ""
        else:
            titulo = noticia.get_text(strip=True)
            link_tag = noticia.find("a")
            link = link_tag.get("href") if link_tag else ""
        if link:
            texto += f"{i}. {titulo} \n {link}\n\n"
        else:
            texto += f"{i}. {titulo}\n"

    mensagem.set_content(texto)

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            email_usuario,
            email_senha
        )

        smtp.send_message(mensagem)

    print("E-mail enviado com sucesso!")