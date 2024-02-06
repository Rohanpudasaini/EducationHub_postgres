import os
from contextlib import contextmanager
import psycopg2
from dotenv import load_dotenv

load_dotenv()


@contextmanager
def get_database_cursor():

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
