# from configparser import ConfigParser
import os
from contextlib import contextmanager
import psycopg2
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def get_database_cursor():
    """
    Context manager to yield a cursor to the PostgreSQL database.

    Establishes a connection to a PostgreSQL database using credentials
    obtained from environment variables and yields a cursor for executing
    database operations. Upon exiting the context, the cursor is closed,
    any changes are committed, and the connection is closed. If an exception
    occurs, it prints the error message, rolls back the transaction, and
    ensures that resources are properly released.

    Yields:
        psycopg2.extensions.cursor: A cursor for executing PostgreSQL commands
        through the established connection.

    Environment Variables:
        - host: Database host address.
        - database: Name of the database to connect to.
        - user: Username for authentication.
        - password: Password for authentication.

    Example:
        with get_database_cursor() as cursor:
            cursor.execute("SELECT * FROM table_name;")
            results = cursor.fetchall()
            for row in results:
                print(row)
    """
    host = os.getenv('host')
    database = os.getenv('database')
    user = os.getenv('user')
    password = os.getenv('password')
    config = {"host": host, "database": database,
              "user": user, "password": password}
    try:
        postgress_connection = psycopg2.connect(**config)
        postgress_cursor = postgress_connection.cursor()
        yield postgress_cursor
    except psycopg2.DatabaseError as error:
        print(f"Database Error: {error}")
        postgress_connection.rollback()
    finally:
        if postgress_cursor:
            postgress_cursor.close()

        if postgress_connection:
            postgress_connection.commit()
            postgress_connection.close()


if __name__ == '__main__':
    conn, curr = get_database_cursor()
    curr.execute("""SELECT * FROM students;""")
    print(curr.fetchall())


# def load_database_connection_and_cursor(filename='database/database.ini',
# section='postgresql'):
#     parser = ConfigParser()
#     parser.read(filename)

#     config = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             config[param[0]] = param[1]
#     else:
#         raise Exception(
    # f'Section {section} not found in the {filename} file'
# )

#     # return config
#
