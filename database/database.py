from dotenv import load_dotenv
from psycopg.rows import dict_row
import psycopg
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a URL de conexão do banco de dados
database_url = os.getenv("DATABASE_URL")

# Valida se a variável de ambiente está configurada corretamente
if not database_url:
    raise ValueError("DATABASE_URL não está definida!")

# Estabelece conexão com o PostgreSQL usando a URL fornecida.
# O parâmetro 'row_factory=dict_row' permite que os resultados venham como dicionários.
# A conexão é mantida aberta durante o ciclo de vida da aplicação.
connection = psycopg.connect(database_url, row_factory=dict_row)
print("Conexão estabelecida com sucesso!")


def get_cursor():
    """
    Retorna um cursor ativo para execução de queries SQL no banco de dados.

    O cursor retornado permite realizar operações como SELECT, INSERT, UPDATE, etc.
    Garante que a conexão esteja ativa antes de retornar o cursor.

    Returns:
        psycopg.Cursor: Objeto cursor conectado ao banco de dados, pronto para uso

    Raises:
        ConnectionError: Se a conexão com o banco foi fechada ou interrompida
    """
    if connection.closed:
        raise ConnectionError("A conexão com o banco foi fechada!")

    return connection.cursor()
