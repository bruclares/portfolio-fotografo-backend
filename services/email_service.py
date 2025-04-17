from flask_mail import Message, Mail

mail = Mail()


def enviar_email_recuperacao(email, token):
    link = f"http://localhost:3000/resetar-senha?token={token}"  # trocar quando subir pra vercel
    msg = Message(
        subject="Redefinição de Senha",
        recipients=[email],
        body=f"Para redefinir sua senha, clique no link: {link}",
    )
    mail.send(msg)
