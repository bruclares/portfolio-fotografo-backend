import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
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
connection = psycopg.connect(database_url, row_factory=dict_row)
print("Conexão estabelecida com sucesso!")


def get_cursor():
    """
    Retorna um cursor ativo para execução de queries SQL.

    Garante que a conexão esteja aberta antes de retornar o cursor.
    Ideal para uso em camadas de serviço ou repositório que acessam o banco.
    """
    if connection.closed:
        raise ConnectionError("A conexão com o banco foi fechada!")

    return connection.cursor()
