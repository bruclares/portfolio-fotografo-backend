from database.database import connection, get_cursor
from flask import request


def registrar_log(tipo_log, status):
    try:
        # conexão ao banco de dados
        with get_cursor() as cur:

            # preparação dos dados para fazer a gravação
            ip_usuario = request.remote_addr
            user_agent = request.headers.get("User-Agent")
            url = request.path
            metodo = request.method

            # Insere os dados na tabela de logs
            cur.execute(
                """ INSERT INTO logs (tipo_log, ip_usuario, user_agent, url, metodo, status)
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (tipo_log, ip_usuario, user_agent, url, metodo, status),
            )

        # A conexão faz o commit no banco de dados
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Erro ao registrar log: {e}")
        print(f"Erro ao registrar log: {repr(e)}")
