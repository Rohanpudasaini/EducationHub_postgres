import os
import sys
from cli_app_class import Student, Academy
from display_functions import *


def show_student_rows():
    os.system("clear")
    student = Student.get_student()
    print("Student Name \t\t| |     Student Roll Number \t|| Enrolled List")
    print("")
    for key, values in student.items():
        enrolled_list = []
        result = (Student.get_enrolled_list(key))
        enrolled_string = ''
        if result != None:
            for i in result:
                i = i[0]
                enrolled_list.append((i))
            enrolled_string = ', '.join(enrolled_list)
        name = f"{values['first_name']} {values['last_name']}"
        count = len(name)
        if count < 23:
            name += " "*(23-count)
        print_colored_message(
            f"{name} | |\t {key} \t\t\t|| {enrolled_string}", Colors.YELLOW)

    # Start of student's main menu
    choice = show_student_menu()
    match choice:
        case "1":
            Student.add_student()
            show_student_rows()

        case "2":
            try:
                Student.remove_student()
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928 ", Colors.RED)
                input("Continue... ")
            show_student_rows()

        case "3":
            try:
                Student.show_remaining_fee()
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928 ", Colors.RED)
                input("Continue... ")
            show_student_rows()

        case "4":
            try:
                Student.pay_fee()
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928 ", Colors.RED)
                input("Continue... ")
            show_student_rows()

        case "5":
            try:
                Student.join_course()
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928 ", Colors.RED)
                input("Continue... ")
            show_student_rows()

        case "6":
            try:
                Student.opt_course()
            except ValueError:
                print_colored_message(
                    "Wrong Roll number format \U0001F928	", Colors.RED)
                input("Continue... ")
            show_student_rows()

        case "7":
            Student.change_session()
            show_student_rows()

        case "8":
            # show_main_menu
            return False
        case _:
            # show_student_menu
            return True


def show_university():
    os.system("clear")
    all_academy = Academy.get_courses()
    academy_info = Academy.get_academy()
    print('''Course ID \t\t\t\t\t\t Courses, Academies and Price''')
    for key, values in all_academy.items():
        print("_"*80)
        print_colored_message(f"{key}", Colors.YELLOW)
        print("_"*80)
        print_colored_message(
            f"\t\t\t Academy Name: {academy_info[values['accademy_id']]}", Colors.YELLOW)
        for key2, values2 in values.items():
            print_colored_message(
                f"\t\t\t {key2.strip()}: {values2}", Colors.YELLOW)
    choice = show_courses_menu()
    match choice:

        case "1":
            if  not Academy.add_academy():
                print_colored_message("The Academy with same name already exsist,",
                                  Colors.RED)
                input("Continue..")

        case "2":
            # show_main_menu
            return False
        case _:
            # show_university_menu
            return True


def main():
    show_welcome_screen()
    while True:
        choice = show_main_menu()
        if choice == '1':
            continue_showing = show_student_rows()
            if not continue_showing:
                continue
        elif choice == '2':
            continue_showing = show_university()
            if not continue_showing:
                continue
        elif choice == '3':
            Academy.show_all_course()
        elif choice == '4':
            sys.exit("Exiting the app...")
            # sys,exit(0)

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
