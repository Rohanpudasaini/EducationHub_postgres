import os
import sys
from db_connect import DatabaseHandler
from cli_app_class import Student, Academy
from display_functions import *
import ipdb


def show_student_rows(db_handler, db_config):
    os.system("clear")
    student = Student.get_student(db_handler, db_config)
    roll_list = student.keys()
    # print(student)
    print("Student Name \t\t| |     Student Roll Number \t|| Enrolled List")
    print("")
    for key, values in student.items():
        enrolled_list = []
        result = (Student.get_enrolled_list(key, db_handler, db_config))
        enrolled_string = ''
        if result != None:
            for i in result:
                i = i[0]
                enrolled_list.append((i))
            enrolled_string = ', '.join(enrolled_list)
        name = f"{values['first_name']} {values['last_name']}"
        count = len(name)
        # ipdb.set_trace()
        if count < 23:
            name += " "*(23-count)
        print_colored_message(
            f"{name} | |\t {key} \t\t\t|| {enrolled_string}", Colors.YELLOW)
    choice = show_student_menu()
    match choice:
        case "1":
            Student.add_student(db_handler, db_config, student, roll_list)
            show_student_rows(db_handler, db_config)

        case "2":
            try:
                Student.remove_student(db_handler, db_config)
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928 ", Colors.RED)
                input("Continue... ")
            show_student_rows(db_handler, db_config)

        case "3":
            try:
                Student.show_remaining_fee(db_handler, db_config)
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928 ", Colors.RED)
                input("Continue... ")
            show_student_rows(db_handler, db_config)

        case "4":
            try:
                Student.pay_fee(student, db_handler, db_config)
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928 ", Colors.RED)
                input("Continue... ")
            show_student_rows(db_handler, db_config)

        case "5":
            try:
                Student.join_course(db_handler, db_config)
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928 ", Colors.RED)
                input("Continue... ")
            show_student_rows(db_handler, db_config)

        case "6":
            try:
                Student.opt_course(db_handler, db_config)
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928	", Colors.RED)
                input("Continue... ")
            show_student_rows(db_handler, db_config)

        case "7":
            Student.change_session(db_handler, db_config)
            show_student_rows(db_handler, db_config)

        case "8":
            # show_main_menu()
            return False
        case _:
            # show_student_rows(db_handler)
            return True


def show_university(db_handler, db_config):
    os.system("clear")
    all_academy = Academy.get_courses(db_handler, db_config)
    academy_info = Academy.get_academy(db_handler, db_config)
    print('''Course ID \t\t\t\t\t\t Courses, Academies and Price''')
    for key, values in all_academy.items():
        print("_"*80)
        print_colored_message(f"{key}", Colors.YELLOW)
        print("_"*80)
        print_colored_message(
            f"\t\t\t Academy Name:: {academy_info[values['accademy_id']]}", Colors.YELLOW)
        for key2, values2 in values.items():
            print_colored_message(
                f"\t\t\t {key2.strip()}: {values2}", Colors.YELLOW)
    choice = show_courses_menu()
    match choice:
        # case "1":
        #     Academy.add_academy(all_academy,db_handler)
        # case "2":
        #     Academy.remove_academy(all_academy, db_handler)
        case "1":
            # show_main_menu()
            return False
        case _:
            # show_university(db_handler)
            return True


def main():
    show_welcome_screen()
    db_handler = DatabaseHandler()
    db_config = db_handler.start_db_handeling()
    Student.start_db_handeling()
    Academy.start_db_handeling()
    while True:
        choice = show_main_menu()
        if choice == '1':
            continue_showing = show_student_rows(db_handler, db_config)
            if not continue_showing:
                continue
        elif choice == '2':
            continue_showing = show_university(db_handler, db_config)
            if not continue_showing:
                continue
        elif choice == '3':
            Academy.show_all_course(db_handler, db_config)
        elif choice == '4':
            sys.exit("Exiting the app...")
            # sys,exit(0)

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
