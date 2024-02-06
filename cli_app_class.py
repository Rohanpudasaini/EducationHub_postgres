import os
from db_handler import DBHandler
from display_functions import print_colored_message, Colors


class Student:

    @classmethod
    def pay_fee(cls):
        """
        Processes the fee payment for a specific student.

        """
        student = DBHandler.get_student()
        # student = cls.get_student(DBHandler,db_config)
        try:
            roll_num_to_pay = int(
                input("Enter the roll number to get pay fee: "))
        except ValueError:
            roll_num_to_pay = int(
                input("Invalid roll number format, please check roll number and enter again: "))
        if roll_num_to_pay in student:
            remaining_fee = 'remaning'
            cash_status = "paying"
            fee = cls.get_remaining_payment(roll_num_to_pay)
            refund = False
            if fee < 0:
                remaining_fee = "overpaid"
                cash_status = "refunding"
                fee = fee * -1
                refund = True

            print(
                f"The student have {fee} fee {remaining_fee}, {cash_status} the fee now.")
            # student = Student.get_student()
            if not refund:
                student[int(roll_num_to_pay)]["total_paid"] = float(
                    student[int(roll_num_to_pay)]["total_paid"]) + fee
            else:
                student[int(roll_num_to_pay)]["total_paid"] = student[int(
                    roll_num_to_pay)]["total_paid"] - fee

            DBHandler.update_student(roll_num_to_pay, tuple(
                (student[roll_num_to_pay]).values()))
        else:
            print_colored_message(
                f"No student with roll number {roll_num_to_pay}", Colors.RED)
        input("\n\nEnter anykey to continue....")

    @classmethod
    def show_remaining_fee(cls):

        student = DBHandler.get_student()
        try:
            roll_num_to_fee = int(
                input("Enter the roll number to get remaning fee: "))
        except ValueError:
            roll_num_to_fee = int(
                input("Invalid roll number format, please check roll number and enter again: "))
        if roll_num_to_fee in student:
            fee = cls.get_remaining_payment(roll_num_to_fee)
            if fee < 0:
                fee = str(
                    fee * -1) + " Overpaid, please check accounts for refund or enroll to any other course."
            else:
                fee = str(fee) + " Remaning, please pay the fee at time"
            print(fee)
        else:
            print_colored_message(
                f"No student with roll number {roll_num_to_fee}", Colors.RED)
        input("\n\nPress anykey to continue...")

    @classmethod
    def join_course(cls):

        try:
            roll_number_to_join = int(
                input("Enter the roll number to get Join a course: "))
        except ValueError:
            roll_number_to_join = int(
                input("Invalid roll number format, please check roll number and enter again: "))
        Academy.show_all_course()
        all_course_list = Academy.get_courses()
        while True:
            try:
                course_id_to_add = int(
                    input("Enter the Course ID of the course you want to add:  ").strip())
                break
            except ValueError:
                print("Please Enter number only")

        if course_id_to_add in all_course_list:
            student_already_enrolled = Academy.if_student_enrolled(
                roll_number_to_join, course_id_to_add)
            if not student_already_enrolled:
                DBHandler.join_course(roll_number_to_join, course_id_to_add)
                cls.update_total_price(roll_number_to_join)
            else:
                print_colored_message(
                    f"The User with roll number {roll_number_to_join} is already enrolled into {course_id_to_add} course",
                    Colors.RED)
        else:
            print_colored_message("No Such Course ID", Colors.RED)
        input("\n Press any key to continue")

    @staticmethod
    def remove_student():

        try:
            roll_num_to_remove = int(
                input("Enter the roll number to remove: "))
        except ValueError:
            roll_num_to_remove = int(
                input("""Invalid roll number format, please check roll number and enter again: """))

        student = DBHandler.get_student()
        if roll_num_to_remove in student:
            DBHandler.remove_student(roll_num_to_remove)
        else:
            print_colored_message(
                f"No student with roll number {roll_num_to_remove}",
                Colors.RED)
        input("\n\nPress anykey to continue...")

    @classmethod
    def opt_course(cls):

        try:
            roll_number_to_opt = int(
                input("Enter the roll number to get Opt from a course: "))
        except ValueError:
            roll_number_to_opt = int(
                input("Invalid roll number format, please check roll number and enter again: "))

        Academy.show_all_course(show=True)
        try:
            course_id_to_remove = int(
                input("Enter the ID of the course you want to remove:  "))
        except ValueError:
            course_id_to_remove = int(
                input("Invalid roll number format, please check roll number and enter again: "))
        courses = DBHandler.get_courses()
        course_ids_list = list(courses.keys())
        if course_id_to_remove in course_ids_list:
            DBHandler.opt_course(roll_number_to_opt, course_id_to_remove)
            cls.update_total_price(int(roll_number_to_opt))
        else:
            print_colored_message("No Such Course ID", Colors.RED)
            input()

    @staticmethod
    def change_session():

        print_colored_message("\n\t\tChanging Session", Colors.GREEN)
        student = DBHandler.get_student()
        for key, values in student.items():
            remaning = Student.get_remaining_payment(int(key))
            if remaning > 0:
                print_colored_message(
                    f"\t\tThe Student {values['first_name']} have {remaning} fee, please check whith him/her once", Colors.RED)
            if remaning < 0:
                remaning = remaning * -1
                print_colored_message(
                    f"\t\tThe Student {values['first_name']} {values['last_name']} have {remaning} fee over charged, please check whith him/her once",
                    Colors.GREEN)
        input("\n\nContinue ....")

    @staticmethod
    def get_remaining_payment(student_id: int):

        student_data = DBHandler.get_student()
        student = student_data.get(
            student_id, "Can't find the id in our Database")
        if isinstance(student, str):
            return student
        remaining = float(student["total_course_cost"]
                          ) - float(student["total_paid"])
        return remaining

    @staticmethod
    def update_total_price(student_id):

        student_data = DBHandler.get_student()
        all_course_list = DBHandler.get_courses()
        student_course_list = DBHandler.get_student_all_courses(student_id)
        student_course_list = list(map(lambda x: x[1], student_course_list))
        total_course_price = 0
        for course in student_course_list:
            total_course_price += all_course_list[course]['course_price']
        student_data[student_id]["total_course_cost"] = total_course_price
        DBHandler.update_student(student_id, tuple(
            (student_data[student_id]).values()))

    @staticmethod
    def get_student():

        return DBHandler.get_student()

    @staticmethod
    def update_student(roll_num_to_pay, student):

        return DBHandler.update_student(roll_num_to_pay, student)

    @staticmethod
    def get_enrolled_list(student_id):

        return DBHandler.get_enrolled_list(student_id)

    @staticmethod
    def add_student():

        full_name = input(
            "\n\nEnter Students full name i.e name and surname only: ").split(" ", 1)
        if len(full_name) == 2:
            firstname, lastname = full_name
        else:
            firstname = "".join(full_name)
            lastname = ""
        print_colored_message(
            "Your new roll number will be assigned automatically at the end, please wait...",
            Colors.YELLOW)

        while True:
            try:
                current_paid = int(input("Enter the current price paid: "))
                break
            except ValueError:
                print_colored_message(
                    "Wrong fee format, please use digit only. \U0001F928 ",
                    Colors.RED)
        student_tuple = (firstname, lastname, current_paid)
        DBHandler.add_student(student_tuple)


class Academy:

    @staticmethod
    def add_academy():

        academy_name = input(
            "Enter the name of the academy that you want to add: ")
        academy_data = DBHandler.get_academies()
        print(academy_data)
        input()
        if academy_name not in academy_data.values():
            DBHandler.add_academy(academy_name)
            return True
        return False

    @staticmethod
    def show_all_course(show=False):

        if not show:
            os.system("clear")
        all_course_list = DBHandler.get_courses()
        print('''Course ID \t Course Name \t\t\t\t\t\t\t Course Price''')
        print("_"*100)
        for value, row in all_course_list.items():
            key = row["course_name"].strip()
            if len(key) < 50:
                key += " " * (50-len(key))
            print_colored_message(
                f"{value}\t   {key} \t:\t {row['course_price']}",
                Colors.YELLOW)
        input("\n\nContinue...")

    @staticmethod
    def get_courses():

        return DBHandler.get_courses()

    @staticmethod
    def if_student_enrolled(student_id, course_id):

        return DBHandler.get_student_courses(student_id, course_id)

    @staticmethod
    def get_academy():

        return DBHandler.get_academies()
