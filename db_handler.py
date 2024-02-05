import psycopg2
from database.config import load_config
from functools import reduce


def get_student():
    """
    Fetches all students from the database and returns them as a dictionary.

    Retrieves every student's details from the 'students' table, orders them by their roll number, and formats the results into a dictionary with roll numbers as keys.

    Returns:
        dict: A dictionary where each key is a student's roll number and its value is another dictionary with keys 'first_name', 'last_name', 'total_course_cost', and 'total_paid' representing the student's details.

    Raises:
        psycopg2.DatabaseError: If a database operation fails.
    """
    command = """SELECT * FROM students
        ORDER BY roll_number ASC;"""
    try:
        connection, cursor = load_config()
        cursor.execute(command)
        result_student = cursor.fetchall()
        if len(result_student) != 0:
            return (reduce(lambda students_dict, x: (students_dict.update({x[0]: {"first_name": x[1], "last_name": x[2], "total_course_cost": x[3], "total_paid": x[4]}})) or students_dict, result_student, {}))

    except psycopg2.DatabaseError as error:
        print(error)

    finally:
        cursor.close()
        connection.close()


def get_courses():
    """
    Fetches all courses from the database and returns them as a dictionary.

    Retrieves every course's details from the 'courses' table and formats the results into a dictionary with course IDs as keys.

    Returns:
        dict: A dictionary where each key is a course ID and its value is another dictionary with keys 'accademy_id', 'course_name', and 'course_price' representing the course's details.

    Raises:
        psycopg2.DatabaseError: If a database operation fails.
    """
    command = """SELECT * FROM courses;"""
    try:
        connection, cursor = load_config()
        cursor.execute(command)
        result_courses = cursor.fetchall()
        if len(result_courses) != 0:
            return (reduce(lambda course_dict, x: (course_dict.update({x[0]: {"accademy_id": x[1], "course_name": x[2], "course_price": x[3]}})) or course_dict, result_courses, {}))
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        cursor.close()
        connection.close()


def get_academies():
    """
    Fetches all academies from the database and returns them as a dictionary.

    Retrieves every academy's details from the 'academies' table and formats the results into a dictionary with academy IDs as keys and their names as values.

    Returns:
        dict: A dictionary where each key is an academy ID and its value is the academy's name.

    Raises:
        psycopg2.DatabaseError: If a database operation fails.
    """
    command = """SELECT * FROM academies;"""
    try:
        connection, cursor = load_config()
        cursor.execute(command)
        resultant_academy = cursor.fetchall()
        dict_academy = {}
        for row in resultant_academy:
            dict_academy.update({row[0]: row[1]})
        return (dict_academy)
    except psycopg2.DatabaseError as error:
        print(error)

    finally:
        cursor.close()
        connection.close()


def get_enrolled_list(id):
    """
    Fetches a list of courses in which a student, identified by their ID, is enrolled.

    Args:
        id (int): The student's ID.

    Returns:
        list: A list of course names the student is enrolled in.

    Raises:
        psycopg2.DatabaseError: If a database operation fails.
    """
    command = """SELECT * FROM student_courses WHERE student_id = (%s);"""
    try:
        connection, cursor = load_config()
        cursor.execute(command, (id,))
        result_enrolled_list = cursor.fetchall()

        # The data from database comes in format `[(1, 1), (1, 4), (1, 2)]`
        result_enrolled_list = list(
            map(lambda result: result[1], result_enrolled_list))
        # Convert the above format into `[1, 4, 2]`

        return (get_course_name(result_enrolled_list))
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        cursor.close()
        connection.close()


def get_course_name(enrolled_list):
    """
    Fetches the names of courses given a list of course IDs.

    Args:
        enrolled_list (list): A list of course IDs.

    Returns:
        list: A list of course names corresponding to the provided course IDs.

    Raises:
        psycopg2.DatabaseError: If a database operation fails.
    """
    if len(enrolled_list) != 0:
        command = """SELECT course_name FROM COURSES WHERE course_id IN %s;"""
        try:
            connection, cursor = load_config()
            cursor.execute(command, (tuple(enrolled_list),))
            result = cursor.fetchall()
            return result
        except psycopg2.DatabaseError as error:
            print(error)
        finally:
            cursor.close()
            connection.close()


def add_student(student_tuple):
    """
    Adds a new student to the database.

    Args:
        student_tuple (tuple): A tuple containing the new student's first name, last name, and the total amount paid.

    Raises:
        psycopg2.DatabaseError: If the student cannot be added due to a database operation failure.
    """

    command = """INSERT INTO students(first_name,last_name,total_paid) VALUES (%s,%s,%s);"""
    try:
        connection, cursor = load_config()
        cursor.execute(command, student_tuple)
        connection.commit()

    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        cursor.close()
        connection.close()


def update_student(roll_no, student):
    """
    Updates the details of an existing student in the database.

    Args:
        roll_no (int): The student's roll number.
        student (tuple): A tuple containing the updated details of the student.

    Raises:
        psycopg2.DatabaseError: If the student's details cannot be updated due to a database operation failure.
    """
    new_tuple = (student) + (roll_no,)
    command = "UPDATE students SET first_name = (%s), last_name= (%s), total_course_cost= (%s), total_paid= (%s) WHERE roll_number= (%s);"
    try:
        connection, cursor = load_config()
        cursor.execute(command, new_tuple)
        connection.commit()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        cursor.close()
        connection.close()


def remove_student(id):
    """
    Deletes a student from the database based on their roll number.

    Args:
        id (int): The roll number of the student to be removed.

    Raises:
        psycopg2.DatabaseError: If the student cannot be removed due to a database operation failure.
    """
    command = """DELETE FROM students WHERE roll_number =(%s);"""
    try:
        connection, cursor = load_config()
        cursor.execute(command, (id,))
        connection.commit()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        cursor.close()
        connection.close()


def get_student_courses(student_id, course_id):
    """
    Checks if a student is enrolled in a specific course.

    Args:
        student_id (int): The student's ID.
        course_id (int): The course ID.

    Returns:
        list: A list containing the enrollment details if found.

    Raises:
        psycopg2.DatabaseError: If the operation fails due to a database error.
    """
    command = """SELECT * FROM student_courses WHERE student_id = (%s) AND course_id = (%s)"""
    new_tuple = (student_id, course_id)
    try:
        connection, cursor = load_config()
        cursor.execute(command, new_tuple)
        return cursor.fetchall()

    except psycopg2.DatabaseError as error:
        print(error)

    finally:
        cursor.close()
        connection.close()


def get_student_all_courses(student_id):
    """
    Fetches all courses a student is enrolled in.

    Args:
        student_id (int): The student's ID.

    Returns:
        list: A list of all courses the student is enrolled in.

    Raises:
        psycopg2.DatabaseError: If the operation fails due to a database error.
    """
    command = """SELECT * FROM student_courses WHERE student_id = (%s) """
    new_tuple = (student_id,)
    try:
        connection, cursor = load_config()
        cursor.execute(command, new_tuple)
        return cursor.fetchall()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        cursor.close()
        connection.close()


def join_course(student_id, course_id):
    """
    Enrolls a student in a course.

    Args:
        student_id (int): The student's ID to enroll.
        course_id (int): The course ID to enroll the student in.

    Raises:
        psycopg2.DatabaseError: If the enrollment operation fails due to a database error.
    """
    command = """INSERT INTO student_courses(student_id,course_id) VALUES (%s,%s)"""
    try:
        connection, cursor = load_config()
        cursor.execute(command, (student_id, course_id))
        connection.commit()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        cursor.close()
        connection.close()


def opt_course(student_id, course_id):
    """
    Unenrolls a student from a course.

    Args:
        student_id (int): The student's ID to unenroll.
        course_id (int): The course ID from which to unenroll the student.

    Raises:
        psycopg2.DatabaseError: If the unenrollment operation fails due to a database error.
    """
    command = "DELETE FROM student_courses WHERE student_id=(%s) AND course_id=(%s)"
    try:
        connection, cursor = load_config()
        cursor.execute(command, (student_id, course_id))
        connection.commit()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    #  initilize_db(load_db_config())

    # db_config = start_db_handeling()
    students = get_student()
    academies = get_academies()
    cources = get_courses()
