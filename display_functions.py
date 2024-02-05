import os


def show_student_menu():
    print_colored_message("\n\t\t\t1. Add Student", Colors.GREEN)
    print_colored_message("\t\t\t2. Remove Student", Colors.RED)
    print_colored_message("\t\t\t3. Get Remaning Fee", Colors.BLUE)
    print_colored_message("\t\t\t4. Pay Remaning Fee", Colors.BLUE)
    print_colored_message("\t\t\t5. Join Courses", Colors.BLUE)
    print_colored_message("\t\t\t6. Opt Courses", Colors.BLUE)
    print_colored_message("\t\t\t7. Move session", Colors.BLUE)
    print_colored_message("\t\t\t8. Exit", Colors.RED)
    print("\n\n\n\n")
    choice = input("\t\t\t\t\tEnter your choice: ")
    return choice


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'


def print_colored_message(message, color):
    print(color + message + Colors.RESET)


def show_main_menu():
    os.system('clear')
    print("\n\n\n\n")
    print_colored_message("\t\t\t\t\t\t1. Student", Colors.GREEN)
    print_colored_message("\t\t\t\t\t\t2. University", Colors.BLUE)
    print_colored_message("\t\t\t\t\t\t3. Courses", Colors.MAGENTA)
    print_colored_message("\t\t\t\t\t\t4. Exit", Colors.RED)
    print("\n\n\n\n")
    choice = input("\t\t\t\t\tEnter your choice: ")
    return choice


def show_welcome_screen():
    os.system("clear")
    print_colored_message(
        "\n\n\t\t\t\t\t\tWelcome to the Educational App!\n\n\n\n", Colors.CYAN)
    print_colored_message('''
                                                                                                                        
    _/_/_/_/        _/                                  _/      _/                          _/    _/            _/       
   _/          _/_/_/  _/    _/    _/_/_/    _/_/_/  _/_/_/_/        _/_/    _/_/_/        _/    _/  _/    _/  _/_/_/    
  _/_/_/    _/    _/  _/    _/  _/        _/    _/    _/      _/  _/    _/  _/    _/      _/_/_/_/  _/    _/  _/    _/   
 _/        _/    _/  _/    _/  _/        _/    _/    _/      _/  _/    _/  _/    _/      _/    _/  _/    _/  _/    _/    
_/_/_/_/    _/_/_/    _/_/_/    _/_/_/    _/_/_/      _/_/  _/    _/_/    _/    _/      _/    _/    _/_/_/  _/_/_/       
                                                                                                                         
                                                                                                                                                                                                                                                                                                                                              
''', color=Colors.GREEN)
    input("\t\t\t\tPress any key to continue...")


def show_courses_menu():
    # print_colored_message("\n\t\t\t1. Add Academy",Colors.GREEN)
    # print_colored_message("\t\t\t2. Remove Academy",Colors.BLUE)
    print_colored_message("\n\t\t\t1. Exit", Colors.RED)
    print("\n\n\n\n")
    choice = input("\t\t\t\t\tEnter your choice: ")
    return choice
