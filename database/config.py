# from configparser import ConfigParser
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()


def load_database_connection_and_cursor():
    host = os.getenv('host')
    database = os.getenv('database')
    user = os.getenv('user')
    password = os.getenv('password')
    config = {"host": host, "database": database,
              "user": user, "password": password}
    postgress_connection = psycopg2.connect(**config)
    postgress_cursor = postgress_connection.cursor()
    return postgress_connection, postgress_cursor


if __name__ == '__main__':
    conn, curr = (load_database_connection_and_cursor())
    curr.execute("""SELECT * FROM students;""")
    print(curr.fetchall())


# def load_database_connection_and_cursor(filename='database/database.ini', section='postgresql'):
#     parser = ConfigParser()
#     parser.read(filename)

#     config = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             config[param[0]] = param[1]
#     else:
#         raise Exception(f'Section {section} not found in the {filename} file')

#     # return config
#
