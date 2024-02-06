"""Imports to get reduce function and databse cursor from `database.config`"""
from functools import reduce
from database.config import get_database_cursor


class DBHandler:

    @classmethod
    def get_enrolled_list(cls, student_id):
        
        command = """SELECT * FROM student_courses WHERE student_id = (%s);"""

        with get_database_cursor() as cursor:
            cursor.execute(command, (student_id,))
            result_enrolled_list = cursor.fetchall()

            # The data from database comes in format `[(1, 1), (1, 4), (1, 2)]`
            result_enrolled_list = list(
                map(lambda result: result[1], result_enrolled_list))
            # Convert the above format into `[1, 4, 2]`

            return cls.get_course_name(result_enrolled_list)

    @staticmethod
    def get_student():
        
        command = """SELECT * FROM students
            ORDER BY roll_number ASC;"""

        with get_database_cursor() as cursor:
            cursor.execute(command)
            result_student = cursor.fetchall()
            if len(result_student) != 0:
                return (reduce(lambda students_dict, x: (students_dict.update({
                    x[0]: {"first_name": x[1], "last_name": x[2], "total_course_cost": x[3],
                           "total_paid": x[4]}})) or students_dict, result_student, {}))

    @staticmethod
    def get_courses():
        
        command = """SELECT * FROM courses;"""

        with get_database_cursor() as cursor:
            cursor.execute(command)
            result_courses = cursor.fetchall()
            if len(result_courses) != 0:
                return (reduce(lambda course_dict, x: (course_dict.update({
                    x[0]: {"accademy_id": x[1], "course_name": x[2], "course_price": x[3]}}))
                    or course_dict, result_courses, {}))

    @staticmethod
    def get_academies():
        
        command = """SELECT * FROM academies;"""

        with get_database_cursor() as cursor:
            cursor.execute(command)
            resultant_academy = cursor.fetchall()
            dict_academy = {}
            for row_academy in resultant_academy:

                # map into dict_academy{academy_id:academy_name}
                dict_academy.update({row_academy[0]: row_academy[1]})
            return dict_academy

    @staticmethod
    def get_course_name(enrolled_list):
        
        if len(enrolled_list) != 0:
            command = """SELECT course_name FROM COURSES WHERE course_id IN %s;"""

            with get_database_cursor() as cursor:
                cursor.execute(command, (tuple(enrolled_list),))
                result = cursor.fetchall()
                return result

    @staticmethod
    def add_student(student_tuple):

        command = """INSERT INTO students(first_name,last_name,total_paid) VALUES(
            %s,%s,%s
            );"""

        with get_database_cursor() as cursor:
            cursor.execute(command, student_tuple)

    @staticmethod
    def update_student(roll_no, student):
        
        new_tuple = (student) + (roll_no,)
        command = """UPDATE students SET
        first_name = (%s)
        last_name= (%s)
        total_course_cost= (%s),
        total_paid= (%s)
        WHERE roll_number= (%s);"""

        with get_database_cursor() as cursor:
            cursor.execute(command, new_tuple)

    @staticmethod
    def remove_student(student_id):
        
        command = """DELETE FROM students WHERE roll_number =(%s);"""

        with get_database_cursor() as cursor:
            cursor.execute(command, (student_id,))

    @staticmethod
    def get_student_courses(student_id, course_id):
        
        command = """SELECT * FROM student_courses WHERE
        student_id = (%s)
        AND course_id = (%s)"""

        new_tuple = (student_id, course_id)

        with get_database_cursor() as cursor:
            cursor.execute(command, new_tuple)
            return cursor.fetchall()

    @staticmethod
    def get_student_all_courses(student_id):
        
        command = """SELECT * FROM student_courses WHERE student_id = (%s) """
        new_tuple = (student_id,)

        with get_database_cursor() as cursor:
            cursor.execute(command, new_tuple)
            return cursor.fetchall()

    @staticmethod
    def join_course(student_id, course_id):
        
        command = """INSERT INTO student_courses(student_id,course_id) VALUES (
            %s,%s
            )"""

        with get_database_cursor() as cursor:
            cursor.execute(command, (student_id, course_id))

    @staticmethod
    def opt_course(student_id, course_id):
        
        command = """DELETE FROM student_courses WHERE
        student_id=(%s)
        AND course_id=(%s)"""

        with get_database_cursor() as cursor:
            cursor.execute(command, (student_id, course_id))

    @staticmethod
    def add_academy(academy_name):
        
        command = "INSERT INTO academies(academy_name)VALUES (%s);"

        with get_database_cursor() as cursor:
            cursor.execute(command, (academy_name,))


if __name__ == "__main__":
    #  initilize_db(load_db_config())

    # db_config = start_db_handeling()
    handler = DBHandler()
    students = handler.get_student()
    academies = handler.get_academies()
    cources = handler.get_courses()
