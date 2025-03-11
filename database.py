import psycopg
from psycopg.rows import dict_row
import os
  # Para carregar as variáveis de ambiente


database_url = os.getenv("DATABASE_URL")
connection = psycopg.connect(database_url, row_factory=dict_row)

# def get_db():
#     db_params = {
#         "host": "localhost",
#         "dbname": "portifolio_fotografo",
#         "user": 'postgres',
#         "password": 'postgres',
#         "port": 5432
#     }

#     return psycopg.connect(os.getenv("DATABASE_URL"), row_factory=dict_row)