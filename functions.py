from User import User, Course, Folder

def start():
    while True:
        main_menu()
        decision = input('Choose one option: ')
        if decision == '1':
            register_user()
        elif decision == '2':
            print(' — — — User Login — — — \n')
            email = input('Enter email : ')
            password = input('Enter password : ')
            with User(email=email, password=password) as user:
                if user.validate_user() == True:
                    login_user(user)
                else:
                    start()
        elif decision == '3':
            break

def main_menu():
    print(' — — — — MENU — — — -')
    print(' 1. Register')
    print(' 2. Login')
    print(' 3. Logout')
    print(' — — — — — — — — — — \n')

def register_user():
    while True:
        print(' — — — User Registration — — — ')
        email = input('Enter email : ')
        password = input('Enter password : ')
        full_name = input('Enter full name : ')
        with User(email, password, full_name) as newUser:
            newUser.create_user()
            print(' — — — User Registration: Success — — — \n')
            login_user(newUser)

def login_user(user):
    email, _, full_name, _ = user.load_user()
    while True:
        print(f' — — — — WELCOME {full_name} — — — -')
        print(f'Your courses: ')
        for course in user.load_courses():
            print(f"{course} \n")
        print('--- WHAT TO DO NEXT ---')
        print(' 1. Acces Course (id)')
        print(' 2. Register in course(course_id)')
        print(' 3. Create Course(course_name and course_term)')
        print(' 4. Previous page')
        decision = input("Make a choice: ")
        if decision == '1':
            course_id = int(input("Course id of course: "))
            with Course(course_id = course_id) as course:
                course_view(course)
        elif decision == '2':
            course_id = int(input("Course id of course: "))
            user.add_user_to_course(course_id)
        elif decision == '3':
            course_name = input("Name of course: ")
            course_term = input("Term of course: ")
            with Course(course_name = course_name, term = course_term) as course:
                course.create_course()
            print(course.course_id)
            user.add_user_to_course(course.course_id)
        elif decision == '4':
            break

def course_view(course):
    course.load_course()
    course_name = course.course_name
    while True:
        print(f' — — — — WELCOME {course_name} — — — -')
        print(f'Your folders: ')
        for folder in course.load_folders():
            print(f"{folder} \n")
        print('--- WHAT TO DO NEXT ---')
        print(' 1. Acces Folder (id)')
        print(' 2. Search question (id)')
        print(' 3. Previous page (id)')
        decision = input("Make a choice: ")
        if decision == '1':
            folder_id = int(input("folder id of folder: "))
            with Folder(folder_id = folder_id) as folder:
                folder_view(folder)
        elif decision == '2':
            pass
        elif decision == '3':
            break

def search_post(course):
    pass
    
def folder_view(folder):
    folder.load_folder()
    folder_name = folder.folder_name
    while True:
        print(f' — — — — WELCOME {folder_name} — — — -')
        print(f'Your posts: ')
        for post in folder.load_posts():
            print(f"{post} \n")
        print('--- WHAT TO DO NEXT ---')

def thread_view(post):
    pass

def post_view(thread):

