from database.database import connection, get_cursor
from flask import request


def registrar_log(tipo_log, status):
    """
    Registra informações de log no banco de dados para auditoria e rastreabilidade.

    A função captura automaticamente os seguintes dados da requisição:
        - IP do usuário
        - User-Agent (navegador ou ferramenta usada)
        - URL acessada
        - Método HTTP utilizado (GET, POST, etc.)

    Args:
        tipo_log (str): Categoria ou tipo do evento registrado.
                        Ex: 'Login bem-sucedido', 'Erro ao salvar contato', 'Cadastro realizado'.
        status (str): Descrição detalhada do evento ocorrido.

    Returns:
        None: A função não retorna valor, mas insere um registro na tabela `logs`.

    Raises:
        Exception: Se ocorrer erro ao inserir o log no banco.
                   O erro é capturado internamente e exibido no console,
                   mas não interrompe a execução principal.
    """

    try:
        with get_cursor() as cur:

            ip_usuario = request.remote_addr
            user_agent = request.headers.get("User-Agent")
            url = request.path
            metodo = request.method

            cur.execute(
                """ INSERT INTO logs (tipo_log, ip_usuario, user_agent, url, metodo, status)
                VALUES (%s, %s, %s, %s, %s, %s) """,
                (tipo_log, ip_usuario, user_agent, url, metodo, status),
            )

        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"Erro ao registrar log: {e}")
        print(f"Erro ao registrar log: {repr(e)}")
