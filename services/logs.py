from database.database import connection, get_cursor
from flask import request


def registrar_log(tipo_log, status):
    """
    Registra informações de log no banco de dados para fins de auditoria e rastreabilidade.

    Parâmetros esperados:
        - tipo_log (str): Tipo ou categoria do log (ex: 'Login', 'Erro', 'Cadastro').
        - status (str): Mensagem descritiva ou status do evento ocorrido.

    Dados registrados automaticamente:
        - IP do usuário
        - User-Agent (navegador ou ferramenta usada)
        - URL acessada
        - Método HTTP (GET, POST etc.)
    """
    try:
        # Abre conexão com o banco e obtém cursor
        with get_cursor() as cur:

            # Coleta dados da requisição
            ip_usuario = request.remote_addr
            user_agent = request.headers.get("User-Agent")
            url = request.path
            metodo = request.method

            # Insere os dados na tabela de logs
            cur.execute(
                """ INSERT INTO logs (tipo_log, ip_usuario, user_agent, url, metodo, status)
                VALUES (%s, %s, %s, %s, %s, %s) """,
                (tipo_log, ip_usuario, user_agent, url, metodo, status),
            )

        # Confirma a transação no banco
        connection.commit()

    except Exception as e:
        # Desfaz qualquer alteração no banco e exibe erro no console
        connection.rollback()
        print(f"Erro ao registrar log: {e}")
        print(f"Erro ao registrar log: {repr(e)}")
