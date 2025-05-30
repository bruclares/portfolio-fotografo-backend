from flask_mail import Message, Mail
from flask import current_app

mail = Mail()


def enviar_email_recuperacao(email, token):
    """
    Envia um e-mail contendo o link de redefinição de senha para o usuário.

    O link inclui o token fornecido como parâmetro e varia conforme o ambiente:
        - Desenvolvimento: usa localhost
        - Produção: usa domínio definido nas configurações

    Args:
        email (str): Endereço de e-mail do destinatário.
        token (str): Token seguro gerado para redefinir a senha.

    Returns:
        None: A função envia o e-mail diretamente e não retorna valor.

    Raises:
        Exception: Se ocorrer erro ao enviar o e-mail (não tratado explicitamente aqui).
    """

    if current_app.config["ENVIRONMENT"] == "development":
        link = f"http://localhost:5500/admin/criar-nova-senha.html?token={token}"
    else:
        link = f"https://portfolio-fotografo-backend.vercel.app/resetar-senha?token= {token}"

    msg = Message(
        subject="Redefinição de Senha",
        recipients=[email],
    )

    msg.html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Redefinir Senha</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">

  <table width="100%" style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
    <tr>
      <td style="text-align: center;">
        <h2 style="color: #333;">Redefinição de Senha</h2>
        <p style="font-size: 16px; color: #555;">
          Olá!
        </p>
        <p style="font-size: 16px; color: #555;">
          Recebemos uma solicitação para redefinir sua senha.
          Clique no botão abaixo para criar uma nova senha:
        </p>
        <a href="{link}" style="display: inline-block; margin-top: 20px; padding: 12px 20px; background-color: #f428f9; color: #ffffff; text-decoration: none; border-radius: 5px; font-size: 16px;">
          Redefinir Senha
        </a>
        <p style="font-size: 14px; color: #999; margin-top: 30px;">
          Se você não solicitou essa alteração, apenas ignore este e-mail.
        </p>
        <p style="font-size: 14px; color: #ccc; margin-top: 10px;">
          — Equipe do Seu App
        </p>
      </td>
    </tr>
  </table>

    </body>
    </html>
    """

    mail.send(msg)
