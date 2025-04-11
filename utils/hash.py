import bcrypt


def verificar_senha(senha_digitada, senha_hash):
    print("HASH RECEBIDO:", repr(senha_hash))
    return bcrypt.checkpw(senha_digitada.encode("utf-8"), senha_hash.encode("utf-8"))
