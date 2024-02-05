from database.config import get_database_cursor
from functools import reduce


def get_student():
    """
    Fetches all students from the database and returns them as a dictionary.

    Retrieves every student's details from the 'students' table, orders them
    by their roll number, and formats the results into a dictionary with roll
    numbers as keys.

    Returns:
        dict: A dictionary where each key is a student's roll number and its
        value is another dictionary with keys 'first_name', 'last_name'
        'total_course_cost', and 'total_paid' representing the student's
        details.

    Raises:
        psycopg2.DatabaseError: If a database operation fails.
    """
    COMMAND = """SELECT * FROM students
        ORDER BY roll_number ASC;"""

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND)
        result_student = cursor.fetchall()
        if len(result_student) != 0:
            return (reduce(lambda students_dict, x: (students_dict.update({
                x[0]: {"first_name": x[1], "last_name": x[2],"total_course_cost": x[3], "total_paid": x[4]}})) or students_dict, result_student, {}))


def get_courses():
    """
    Fetches all courses from the database and returns them as a dictionary.

    Retrieves every course's details from the 'courses' table and formats the
    results into a dictionary with course IDs as keys.

    Returns:
        dict: A dictionary where each key is a course ID and its value is
        another dictionary with keys 'accademy_id', 'course_name', and
        'course_price' representing the course's details.

    Raises:
        psycopg2.DatabaseError: If a database operation fails.
    """
    COMMAND = """SELECT * FROM courses;"""

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND)
        result_courses = cursor.fetchall()
        if len(result_courses) != 0:
            return (reduce(lambda course_dict, x: (course_dict.update({x[0]: {"accademy_id": x[1], "course_name": x[2], "course_price": x[3]}})) or course_dict, result_courses, {}))


def get_academies():
    """
    Fetches all academies from the database and returns them as a dictionary.

    Retrieves every academy's details from the 'academies' table and formats
    the results into a dictionary with academy IDs as keys and their names as
    values.

    Returns:
        dict: A dictionary where each key is an academy ID and its value is
        the academy's name.

    Raises:
        psycopg2.DatabaseError: If a database operation fails.
    """
    COMMAND = """SELECT * FROM academies;"""

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND)
        resultant_academy = cursor.fetchall()
        dict_academy = {}
        for row_academy in resultant_academy:

            # map into dict_academy{academy_id:academy_name}
            dict_academy.update({row_academy[0]: row_academy[1]})
        return (dict_academy)


def get_enrolled_list(id):
    """
    Fetches a list of courses in which a student, identified by their ID, is
    enrolled.

    Args:
        id (int): The student's ID.

    Returns:
        list: A list of course names the student is enrolled in.

    Raises:
        psycopg2.DatabaseError: If a database operation fails.
    """
    COMMAND = """SELECT * FROM student_courses WHERE student_id = (%s);"""

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND, (id,))
        result_enrolled_list = cursor.fetchall()

        # The data from database comes in format `[(1, 1), (1, 4), (1, 2)]`
        result_enrolled_list = list(
            map(lambda result: result[1], result_enrolled_list))
        # Convert the above format into `[1, 4, 2]`

        return (get_course_name(result_enrolled_list))


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
        COMMAND = """SELECT course_name FROM COURSES WHERE course_id IN %s;"""

        with get_database_cursor() as cursor:
            cursor.execute(COMMAND, (tuple(enrolled_list),))
            result = cursor.fetchall()
            return result


def add_student(student_tuple):
    """
    Adds a new student to the database.

    Args:
        student_tuple (tuple): A tuple containing the new student's first name,
        last name, and the total amount paid.

    Raises:
        psycopg2.DatabaseError: If the student cannot be added due to a
        database operation failure.
    """

    COMMAND = """INSERT INTO students(first_name,last_name,total_paid) VALUES(
        %s,%s,%s
        );"""

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND, student_tuple)


def update_student(roll_no, student):
    """
    Updates the details of an existing student in the database.

    Args:
        roll_no (int): The student's roll number.
        student (tuple): A tuple containing the updated details of the student.

    Raises:
        psycopg2.DatabaseError: If the student's details cannot be updated due
        to a database operation failure.
    """
    new_tuple = (student) + (roll_no,)
    COMMAND = """UPDATE students SET
    first_name = (%s)
    last_name= (%s)
    total_course_cost= (%s),
    total_paid= (%s)
    WHERE roll_number= (%s);"""

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND, new_tuple)


def remove_student(id):
    """
    Deletes a student from the database based on their roll number.

    Args:
        id (int): The roll number of the student to be removed.

    Raises:
        psycopg2.DatabaseError: If the student cannot be removed due to a
        database operation failure.
    """
    COMMAND = """DELETE FROM students WHERE roll_number =(%s);"""

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND, (id,))


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
    COMMAND = """SELECT * FROM student_courses WHERE
    student_id = (%s)
    AND course_id = (%s)"""

    new_tuple = (student_id, course_id)

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND, new_tuple)
        return cursor.fetchall()


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
    COMMAND = """SELECT * FROM student_courses WHERE student_id = (%s) """
    new_tuple = (student_id,)

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND, new_tuple)
        return cursor.fetchall()


def join_course(student_id, course_id):
    """
    Enrolls a student in a course.

    Args:
        student_id (int): The student's ID to enroll.
        course_id (int): The course ID to enroll the student in.

    Raises:
        psycopg2.DatabaseError: If the enrollment operation fails due to a
        database error.
    """
    COMMAND = """INSERT INTO student_courses(student_id,course_id) VALUES (
        %s,%s
        )"""

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND, (student_id, course_id))


def opt_course(student_id, course_id):
    """
    Unenrolls a student from a course.

    Args:
        student_id (int): The student's ID to unenroll.
        course_id (int): The course ID from which to unenroll the student.

    Raises:
        psycopg2.DatabaseError: If the unenrollment operation fails due to a
        database error.
    """
    COMMAND = """DELETE FROM student_courses WHERE
    student_id=(%s)
    AND course_id=(%s)"""

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND, (student_id, course_id))


def add_academy(academy_name):
    """
    Add Adacemy of given name into the academies table of database.

    Args:
        academy_name(string): Name of the academy.

    Raises:
        psycopg2.DatabaseError: If the unenrollment operation fails due to a
        database error.
    """
    COMMAND = "INSERT INTO academies(academy_name)VALUES (%s);"

    with get_database_cursor() as cursor:
        cursor.execute(COMMAND, (academy_name,))


if __name__ == "__main__":
    #  initilize_db(load_db_config())

    # db_config = start_db_handeling()
    students = get_student()
    academies = get_academies()
    cources = get_courses()
