from database.database import connection, get_cursor
from flask import request


def registrar_log(tipo_log, status):
    try:
        with get_cursor() as cur:
           
            ip_usuario = request.remote_addr
            user_agent = request.headers.get("User-Agent")
            url = request.path
            metodo = request.method
            
            cur.execute(
                ''' INSERT INTO logs (tipo_log, ip_usuario, user_agent, url, metodo, status)
                VALUES (%s,%s,%s,%s,%s,%s)
                ''', (tipo_log, ip_usuario, user_agent, url, metodo, status))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Erro ao registrar log: {e}") 
        print(f"Erro ao registrar log: {repr(e)}")