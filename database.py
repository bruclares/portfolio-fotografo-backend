import psycopg
from psycopg.rows import dict_row


def get_db():
    db_params = {
        "host": "localhost",
        "dbname": "portifolio_fotografo",
        "user": 'postgres',
        "password": 'postgres',
        "port": 5432
    }

    return psycopg.connect(**db_params, row_factory=dict_row)