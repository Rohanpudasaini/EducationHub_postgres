import psycopg2
from DB.config import load_config
from functools import reduce


class DatabaseHandler:

    def start_db_handeling(self):
        return load_config()

    @staticmethod
    def initilize_db(db_config):
        """ Connect to the PostgreSQL database server """
        choice = input(
            "This method will erase any data available in the databse, do you want to continue(y/n): ")
        if (choice).lower() == 'n':
            return
        commands = ("""
    CREATE TABLE students (
        roll_number SERIAL PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255),
        total_course_cost INT DEFAULT 0,
        total_paid INT DEFAULT 0,
        total_disc
    );
    """,
                    """
    CREATE TABLE academies(
        academy_id SERIAL PRIMARY KEY,
        academy_name VARCHAR(50) NOT NULL
    );""",
                    """
    CREATE TABLE courses(
        course_id SERIAL PRIMARY KEY,
        academy_id INT REFERENCES academies(academy_id) ON DELETE CASCADE,
        course_name VARCHAR(100) NOT NULL,
        course_price INT NOT NULL
    );""",
                    """
    CREATE TABLE student_courses(
        student_id INT REFERENCES students(roll_number) ON DELETE CASCADE,
        course_id INT REFERENCES courses(course_id) ON DELETE CASCADE,
        PRIMARY KEY (student_id, course_id)
    );
    """)
        try:
            with psycopg2.connect(**db_config) as conn:
                print('Connected to the PostgreSQL server.')
                with conn.cursor() as curr:
                    for command in commands:
                        curr.execute(command)
                    return conn
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)

    @staticmethod
    def get_student(db_config):
        command = """SELECT * FROM students
        ORDER BY roll_number ASC;"""
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command)
                    result = curr.fetchall()
                    if len(result) != 0:
                        return (reduce(lambda students_dict, x: (students_dict.update({x[0]: {"first_name": x[1], "last_name": x[2], "total_course_cost": x[3], "total_paid": x[4]}})) or students_dict, result, {}))

        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def get_courses(db_config):
        command = """SELECT * FROM courses;"""
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command)
                    result = curr.fetchall()
                    if len(result) != 0:
                        return (reduce(lambda course_dict, x: (course_dict.update({x[0]: {"accademy_id": x[1], "course_name": x[2], "course_price": x[3]}})) or course_dict, result, {}))
        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def get_academies(db_config):
        command = """SELECT * FROM academies;"""
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command)
                    result = curr.fetchall()
                    dict_academy = {}
                    for row in result:
                        dict_academy.update({row[0]: row[1]})
                    return (dict_academy)
        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def get_enrolled_list(id, db_config):
        command = """SELECT * FROM student_courses WHERE student_id = (%s);"""
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command, (id,))
                    result = curr.fetchall()
                    result = list(map(lambda x: x[1], result))
                    return (DatabaseHandler.get_course_name(db_config, result))
        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def get_course_name(db_config, enrolled_list):
        if len(enrolled_list) != 0:
            command = """SELECT course_name FROM COURSES WHERE course_id IN %s;"""
            try:
                with psycopg2.connect(**db_config) as conn:
                    with conn.cursor() as curr:
                        curr.execute(command, (tuple(enrolled_list),))
                        result = curr.fetchall()
                        # result =
                        return result
            except psycopg2.DatabaseError as e:
                print(e)

    @staticmethod
    def add_student(db_config, student_tuple):
        # db_config = DatabaseHandler.start_db_handeling(DatabaseHandler)

        command = """INSERT INTO students(first_name,last_name,total_paid) VALUES (%s,%s,%s);"""
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command, student_tuple)
                conn.commit()
                curr.close()
            conn.close()
        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def update_student(db_config, roll_no, student):
        new_tuple = (student) + (roll_no,)
        command = "UPDATE students SET first_name = (%s), last_name= (%s), total_course_cost= (%s), total_paid= (%s) WHERE roll_number= (%s);"
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command, new_tuple)
                conn.commit()
        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def remove_student(db_config, id):
        command = """DELETE FROM students WHERE roll_number =(%s);"""
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command, (id,))
                conn.commit()
        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def get_student_courses(db_config, student_id, course_id):
        command = """SELECT * FROM student_courses WHERE student_id = (%s) AND course_id = (%s)"""
        new_tuple = (student_id, course_id)
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command, new_tuple)
                    return curr.fetchall()

        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def get_student_all_courses(db_config, student_id):
        command = """SELECT * FROM student_courses WHERE student_id = (%s) """
        new_tuple = (student_id,)
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command, new_tuple)
                    return curr.fetchall()
        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def join_course(db_config, student_id, course_id):
        command = """INSERT INTO student_courses(student_id,course_id) VALUES (%s,%s)"""
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command, (student_id, course_id))
                conn.commit()
        except psycopg2.DatabaseError as e:
            print(e)

    @staticmethod
    def opt_course(db_config, student_id, course_id):
        command = "DELETE FROM student_courses WHERE student_id=(%s) AND course_id=(%s)"
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as curr:
                    curr.execute(command, (student_id, course_id))
                conn.commit()
        except psycopg2.DatabaseError as e:
            print(e)


if __name__ == "__main__":
    #  initilize_db(load_db_config())
    db_handler = DatabaseHandler()
    db_config = db_handler.start_db_handeling()
    students = db_handler.get_student(db_config)
    academies = db_handler.get_academies(db_config)
    cources = db_handler.get_courses(db_config)
