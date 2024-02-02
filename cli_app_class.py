# import csv
from db_connect import DatabaseHandler
from display_functions import *
import os
import ipdb

class Student:

    @staticmethod
    def update_total_price(db_handler, db_config,student_id):
        """
        Updates the total cost of courses for the student.

        Args:
            id (int): The roll number of the student.
        """
        student_data = db_handler.get_student(db_config)
        all_course_list = db_handler.get_courses(db_config)
        student_course_list = db_handler.get_student_all_courses(db_config,student_id)
        student_course_list = list(map(lambda x: x[1], student_course_list))
        total_course_price = 0
        for course in student_course_list:
            total_course_price += all_course_list[course]['course_price']
        student_data[student_id]["total_course_cost"] = total_course_price 
        # ipdb.set_trace()
        # total_cost = 0
        # student = db_handler.get_student()
        # for course in student[id]["Enrolled_list"]:
        #     if course != "":
        #         total_cost += int(all_course_list[course])
        # student_data[id]["Total_cost"] = str(total_cost)
        # db_handler.write_student(student_data)
        db_handler.update_student(db_config, student_id, tuple((student_data[student_id]).values()) )

    def get_remaining_payment(self, id, db_handler, db_config):
        """
        Retrieves the remaining payment amount for the student.

        Args:
            id (int): The roll number of the student.

        Returns:
            float: The remaining amount to be paid by the student.
        """
        student_data = db_handler.get_student(db_config)
        student = student_data.get(id, "Can't find the id in our Database")
        if isinstance(student, str):
            return student
        remaining = float(student["total_course_cost"]) - float(student["total_paid"])
        return remaining
    @classmethod
    def start_db_handeling(cls):
        """
        Initializes database handling for the student.
        """
        cls.db_handler = DatabaseHandler()
        cls.db_config = cls.db_handler.start_db_handeling()
        
    
    @staticmethod
    def get_student(db_handler, db_config):
        """
        Retrieves student data from the database.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.

        Returns:
            dict: A dictionary containing student data.
        """
        return db_handler.get_student(db_config)
    
    @staticmethod
    def update_student(db_handler,db_config,roll_num_to_pay,student):
        """
        Writes student data to the database.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
            student (dict): A dictionary containing the student's data.
        """
        return db_handler.update_student(db_config,roll_num_to_pay,student)

    @staticmethod
    def get_enrolled_list(id,db_handler,db_config):
        return db_handler.get_enrolled_list(id, db_config)
    @classmethod
    def add_student(cls,db_handler, db_config,student:dict, roll_list):
        """
        Adds a new student to the database.

        Args:
            student (dict): A dictionary containing the new student's data.
        """
        # try:
        #     last_roll_number = list(student.keys())[-1]
        # except ValueError:
        #     last_roll_number = 0
        full_name = input("\n\nEnter Students full name i.e name and surname only: ").split(" ",1)
        if len(full_name) ==2:
            firstname, lastname = full_name
        else:
            firstname = "".join(full_name)
            lastname = ""
        print_colored_message(f"Your new roll number will be assigned automatically at the end, please wait...",Colors.YELLOW)

        while True:
            try:
                current_paid = int(input("Enter the current price paid: "))
                break
            except ValueError:
                print_colored_message("Wrong fee format, please use digit only. \U0001F928 ",Colors.RED)
        student_tuple = (firstname,lastname,current_paid)
        # if rollnumber  in student:
        #     print_colored_message(f"The User with Roll NO {rollnumber} already exsist. Do you want to edit the user? (y/n):", Colors.RED)
        #     edit = input()
        #     if edit.lower() == "y":
        #         updated_student_tuple = (firstname, lastname,current_paid)
        #         db_handler.update_student(db_config,rollnumber, updated_student_tuple)
        #     else:
        #         print_colored_message('''Redirecting back to the Student page......''', Colors.YELLOW)  
        #         cls.add_student(db_handler,db_config,student)  
        # else:
        cls.db_handler.add_student(db_config,student_tuple)   
    @classmethod
    def remove_student(cls,db_handler,db_config):
        """
        Removes a student from the database based on their roll number.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        try:
            roll_num_to_remove = int(input("Enter the roll number to remove: "))
        except ValueError:
            roll_num_to_remove = int(input("Invalid roll number format, please check roll number and enter again: "))
        student = cls.get_student(db_handler,db_config)
        if roll_num_to_remove in student:
            # student.pop(int(roll_num_to_remove))
            # cls.write_student(db_handler,student)
            cls.db_handler.remove_student(db_config,roll_num_to_remove)
        else:
            print_colored_message(f"No student with roll number {roll_num_to_remove}", Colors.RED)
        input("\n\nPress anykey to continue...")
    @classmethod
    def show_remaining_fee(cls,db_handler, db_config):
        """
        Displays the remaining fee for a specific student.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        student = cls.get_student(db_handler,db_config)
        try:
            roll_num_to_fee = int(input("Enter the roll number to get remaning fee: "))
        except ValueError:
            roll_num_to_fee = int(input("Invalid roll number format, please check roll number and enter again: "))
        if roll_num_to_fee in student:
            fee = cls.get_remaining_payment(Student,roll_num_to_fee,db_handler, db_config)
            if fee < 0:
                fee = str(fee *-1) + " Overpaid, please check accounts for refund or enroll to any other course."
            else:
                fee = str(fee) + " Remaning, please pay the fee at time"
            print(fee)
        else:
            print_colored_message(f"No student with roll number {roll_num_to_fee}",Colors.RED)
        input("\n\nPress anykey to continue...")
    @classmethod
    def pay_fee(student,cls,db_handler, db_config):
        """
        Processes the fee payment for a specific student.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        # student = cls.get_student(db_handler,db_config)
        try:
            roll_num_to_pay = int(input("Enter the roll number to get pay fee: "))
        except ValueError:
            roll_num_to_pay = int(input("Invalid roll number format, please check roll number and enter again: "))
        if roll_num_to_pay in student:
            remaining_fee = 'remaning'
            cash_status = "paying"
            fee = cls.get_remaining_payment(cls,roll_num_to_pay,db_handler, db_config)
            refund = False
            if fee < 0:
                remaining_fee = "overpaid"
                cash_status = "refunding"
                fee = fee * -1
                refund = True

            print(f"The student have {fee} fee {remaining_fee}, {cash_status} the fee now.")
            # student = Student.get_student()
            if not refund:
                student[int(roll_num_to_pay)]["total_paid"] = float(student[int(roll_num_to_pay)]["total_paid"]) + fee
            else:
                student[int(roll_num_to_pay)]["total_paid"] = student[int(roll_num_to_pay)]["total_paid"] - fee *0.85
                
            cls.update_student(db_handler,db_config,roll_num_to_pay,tuple((student[roll_num_to_pay]).values()))
        else:
            print_colored_message(f"No student with roll number {roll_num_to_pay}",Colors.RED)
        input("\n\nEnter anykey to continue....")
    @classmethod
    def join_course(cls, db_handler, db_config):
        """
        Enrolls a student in a new course.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        try:
            roll_number_to_join = int(input("Enter the roll number to get Join a course: "))
        except ValueError:
            roll_number_to_join = int(input("Invalid roll number format, please check roll number and enter again: "))
        Academy.show_all_course(db_handler, db_config)
        all_course_list = Academy.get_courses(db_handler, db_config)
        while True:
            try:
                course_id_to_add = int(input("Enter the Course ID of the course you want to add:  ").strip())
                break
            except ValueError:
                print("Please Enter number only")

        if course_id_to_add in all_course_list:
            student_already_enrolled = Academy.if_student_enrolled(db_handler,db_config,roll_number_to_join,course_id_to_add)
            if not student_already_enrolled:
                db_handler.join_course(db_config, roll_number_to_join,course_id_to_add)
                # cls.update_total_price(cls, roll_number_to_join)
                cls.update_total_price(db_handler,db_config,roll_number_to_join)
            else:
                print_colored_message(f"The User with roll number {roll_number_to_join} is already enrolled into {course_id_to_add} course",Colors.RED)
        else:
            print_colored_message("No Such Course ID", Colors.RED)
        input("\n Press any key to continue")
    @classmethod
    def opt_course(cls,db_handler, db_config):
        """
        Opts a student out of a course.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        try:
            roll_number_to_opt = int(input("Enter the roll number to get Opt from a course: "))
        except ValueError:
            roll_number_to_opt = int(input("Invalid roll number format, please check roll number and enter again: "))
        # show_all_course()
        student = cls.get_student(db_handler, db_config)
        Academy.show_all_course(db_handler, db_config, show=True)
        try:
            course_id_to_remove = int(input("Enter the ID of the course you want to remove:  "))
        except ValueError:
            course_id_to_remove = int(input("Invalid roll number format, please check roll number and enter again: "))
        courses = db_handler.get_courses(db_config)
        # print(list(courses.keys()))
        # print(course_id_to_remove)
        # ipdb.set_trace()
        course_ids_list = list(courses.keys())
        if course_id_to_remove in course_ids_list:
            # student[roll_number_to_opt]["Enrolled_list"].remove(course_id_to_remove)
            # refunded = float(student[int(roll_number_to_opt)]['Total_cost'])
            # paid_total = float(student[int(roll_number_to_opt)]['Paid'])
            # student[int(roll_number_to_opt)]['Paid'] = paid_total - (refunded *0.2)

            # print(student)
            # input() 
            # cls.write_student(db_handler,student)
            db_handler.opt_course(db_config,roll_number_to_opt,course_id_to_remove)
            cls.update_total_price(db_handler,db_config,int(roll_number_to_opt))
        else:
            print_colored_message("No Such Course ID", Colors.RED)
            input()
    @staticmethod
    def change_session(db_handler,db_config):
        """
        Changes the session for all students, checking their fee status.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        print_colored_message("\n\t\tChanging Session",Colors.GREEN)
        student = db_handler.get_student(db_config)
        for key, values in student.items():
            remaning = Student.get_remaining_payment(Student, int(key),db_handler,db_config)
            if  remaning > 0:
                print_colored_message(f"\t\tThe Student {values['first_name']} have {remaning} fee, please check whith him/her once",Colors.RED)
            if  remaning < 0:
                remaning = remaning * -1
                print_colored_message(f"\t\tThe Student {values['first_name']} {values['last_name']} have {remaning} fee over charged, please check whith him/her once",Colors.GREEN)
        input("\n\nContinue ....")

class Academy:
    @classmethod
    def start_db_handeling(cls):
        """
        Initializes database handling for the student.
        """
        cls.db_handler = DatabaseHandler()
        cls.db_config = cls.db_handler.start_db_handeling()
    @staticmethod  
    def add_academy(all_academy,db_handler):
        """
        Adds a new academy and its courses to the database.

        Args:
            all_academy (dict): A dictionary containing all academies and their courses.
            db_handler (DatabaseHandler): A DatabaseHandler object to interact with the database.
        """
        # all_academy, _ =  db_handler.get_course()
        academy_name = input("Enter Name of Academy: ")
        course_detail = input("Enter Academy details like (Coursename:price,coursename2:price) :")
        courses = course_detail.split(",")
        for course in courses:
            courses_name, course_price = course.split(":")
            if academy_name not in all_academy:
                all_academy[academy_name] = {courses_name:course_price}
            else:
                all_academy[academy_name].update({courses_name:course_price})
        db_handler.write_courses(all_academy)
    @staticmethod
    def remove_academy(all_academy,db_handler):
        """
        Removes an academy from the database.

        Args:
            all_academy (dict): A dictionary containing all academies and their courses.
            db_handler (DatabaseHandler): A DatabaseHandler object to interact with the database.
        """
        remove = input("Enter Academy Name: ")
        if remove in all_academy:
            all_academy.pop(remove)
            db_handler.write_courses(all_academy)
        else:
            print_colored_message(f"Cant find the Academy named {remove}",Colors.RED)
        input("\n\nContinue...")
    @staticmethod
    def show_all_course(db_handler, db_config, show=False):
        """
        Displays all courses and their details from the database.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object to interact with the database.
        """
        if not show:
            os.system("clear")
        all_course_list = db_handler.get_courses(db_config)
        # print(all_course_list)
        print('''Course ID \t Course Name \t\t\t\t\t\t\t Course Price''')
        print("_"*100)
        for value, row in all_course_list.items():
            key = row["course_name"].strip()
            if len(key) < 50:
                key += " " * (50-len(key))
            print_colored_message(f"{value}\t   {key} \t:\t {row['course_price']}", Colors.YELLOW)
        input("\n\nContinue...")
    @staticmethod
    def get_courses(db_handler,db_config):
        """
        Retrieves all courses from the database.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object to interact with the database.

        Returns:
            tuple: A tuple containing a dictionary of all courses and their details.
        """
        return db_handler.get_courses(db_config)
    @staticmethod
    def if_student_enrolled(db_handler,db_config,student_id, course_id):
        return db_handler.get_student_courses(db_config,student_id, course_id)
    @staticmethod
    def get_academy(db_handler,db_config):
        return db_handler.get_academies(db_config)

    