"""Dedicated module which contains connectivity logic for the remote Postgres database.
"""
import psycopg2


def open_connection(
    dbname: str,
    user: str,
    password: str,
    host: str = "publications-db",
    port: int = 5432
):
    """Open connection to Postgres database.

    :param dbname: name of database (see `container_name` property)
    :param user: username of service account (typically 'postgres')
    :param password: password of service account (see `POSTGRES_PASSWORD_FILE` property)
    :param host: address of database instance, defaults to "localhost"
    :param port: port on which the database listens for incoming connections, defaults to 5432
    :return: a connection object
    """
    conn_params = { 
        "dbname": dbname, 
        "user": user, 
        "password": password, 
        "host": host, 
        "port": str(port)
    }
    return psycopg2.connect(**conn_params)


if __name__ == "__main__":
    pass