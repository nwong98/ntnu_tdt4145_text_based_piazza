import mysql.connector


connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="AbA.,.123"
)


def init_db():
    cursor = connection.cursor()
    cursor.execute('USE db')


def main_menu():
    print(' — — — — MENU — — — -')
    print(' 1. Register User')
    print(' 2. Login - participant')
    print(' 3. Login - admin')
    print(' 4. Exit')
    print(' — — — — — — — — — — ')


def register_user():
    with connection.cursor() as cursor:
        while True:
            print(' — — — User Registration — — — \n')
            email = input('Enter email : ')
            password = input('Enter password : ')
            full_name = input('Enter full name : ')
            sql = f"INSERT INTO `user` (`email`,`pass`,`full_name`) VALUES ('{email}', '{password}', '{full_name}')"
            try:
                cursor.execute(sql)
                connection.commit()
                print('\n — — — SUCCESS — — — \n')
                break
            except mysql.connector.Error as e:
                print(f"\n{e} \n- - - PLEASE TRY AGAIN - - - \n")


def create_course():
    with connection.cursor() as cursor:
        while True:
            print(' — — — Create Course — — — \n')
            course_name = input('Enter course name : ')
            course_term = input('Enter course term : ')
            sql = f"INSERT INTO `course` (`course_name`,`term`) VALUES ('{course_name}', '{course_term}')"
            try:
                cursor.execute(sql)
                connection.commit()
                print('\n — — — SUCCESS — — — \n')
                break
            except mysql.connector.Error as e:
                print(f"\n{e} \n- - - PLEASE TRY AGAIN - - - \n")

# IKKE FERDIG


def create_folder():
    with connection.cursor() as cursor:
        while True:
            print(' — — — Create Course — — — \n')
            folder_name = input('Enter course name : ')
            course_id = input('Enter course term : ')
            parent_folder = input('Enter if any: ')
            sql = f"INSERT INTO `course` (`course_name`,`term`) VALUES ('{course_name}', '{course_term}')"
            try:
                cursor.execute(sql)
                connection.commit()
                print('\n — — — SUCCESS — — — \n')
                break
            except mysql.connector.Error as e:
                print(f"\n{e} \n- - - PLEASE TRY AGAIN - - - \n")


def add_user_to_course():
    with connection.cursor() as cursor:
        while True:
            print(' — — — Add User To Course — — — \n')
            course_id = input('Enter course ID : ')
            email = input('Enter user email : ')
            sql = f"INSERT INTO `participates_in_course` (`email`,`course_id`) VALUES ('{email}', '{course_id}')"
            try:
                cursor.execute(sql)
                connection.commit()
                print('\n — — — SUCCESS — — — \n')
                break
            except mysql.connector.Error as e:
                print(f"\n{e} \n- - - PLEASE TRY AGAIN - - - \n")


def get_courses():
    with connection.cursor() as cursor:
        while True:
            course_id = input("Enter course ID: ")
            print(' — — — COURSES — — — \n')
            sql = f"SELECT course_id, course_name, term FROM course"
            cursor.execute(sql)
            course_list = cursor.fetchall()
            if len(course_list) != 0:
                for course in course_list:
                    print(
                        f"Course ID: {course[0]} | Course Name: {course[1]} | Course Term: {course[2]}")
                print('\n — — — END — — —')
                break
            else:
                print('Course not found, please try again')
            print('\n — — — END — — —')


def get_folders_in_course():
    with connection.cursor() as cursor:
        while True:
            course_id = input("Enter course ID: ")
            print(' — — — COURSES — — — \n')
            sql = f"SELECT folder_name FROM folder WHERE course_id = '{course_id}'"
            cursor.execute(sql)
            folder_list = cursor.fetchall()
            if len(folder_list) != 0:
                for folder in folder_list:
                    print(f"Folder name: {folder[0]}")
                print('\n — — — END — — —')
                break
            else:
                print('Course not found, please try again')
            print('\n — — — END — — —')


init_db()
register_user()
