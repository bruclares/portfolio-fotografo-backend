import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL não está definida!")

connection = psycopg.connect(database_url, row_factory=dict_row)
print("Conexão estabelecida com sucesso!")


def get_cursor():
    if connection.closed:
        raise ConnectionError("A conexão com o banco foi fechada!")
    return connection.cursor()
