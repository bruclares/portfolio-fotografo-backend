import bcrypt


def verificar_senha(senha_digitada, senha_hash):
    """
    Verifica se a senha fornecida pelo usuário corresponde ao hash armazenado.

    Parâmetros:
        - senha_digitada (str): Senha em texto plano digitada pelo usuário.
        - senha_hash (str): Hash da senha armazenado no banco de dados.

    Retorna:
        - True se a senha for válida, False caso contrário.
    """
    print(
        "HASH RECEBIDO:", repr(senha_hash)
    )  # Log de depuração (pode ser removido em produção)
    return bcrypt.checkpw(senha_digitada.encode("utf-8"), senha_hash.encode("utf-8"))
