from Classes import User, Course, Folder, Thread, Post


def start():
    while True:
        main_menu()
        decision = input('Choose one option: ')
        if decision == '1':
            register_user()
        elif decision == '2':
            print(' — — — User Login — — — \n')
            user_email = input('Enter email : ')
            user_password = input('Enter password : ')
            with User(email=user_email, password=user_password) as user:
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
        user_email = input('Enter email : ')
        user_password = input('Enter password : ')
        user_full_name = input('Enter full name : ')
        with User(user_email, user_password, user_full_name) as newUser:
            newUser.create_user()
            print(' — — — User Registration: Success — — — \n')
            login_user(newUser)


def login_user(user):
    while True:
        print(f' — — — — WELCOME {user.email} — — — -')
        print(f'Your courses: ')
        for course in user.load_courses():
            print(f"{course} \n")
        print('--- WHAT TO DO NEXT ---')
        print(' 1. Acces Course (id)')
        print(' 2. Register in course(course_id)')
        print(' 3. Create Course(course_name and course_term)')
        print(' 4. Previous page')
        decision = input("Make a choice: \n")
        if decision == '1':
            course_id = int(input("Course id of course: "))
            with Course(id=course_id) as course:
                course_view(course, user)
        elif decision == '2':
            for course in user.load_all_courses():
                print(f"{course} \n")
            course_id = int(input("Course id of course: "))
            user.add_user_to_course(course_id)
        elif decision == '3':
            course_title = input("Name of course: ")
            course_term = input("Term of course: ")
            with Course(title=course_title, term=course_term) as course:
                course.create_course()
            print(course.id)
            user.add_user_to_course(course.id)
        elif decision == '4':
            break


def course_view(course, user):
    while True:
        print(f' — — — — WELCOME {course.title} — — — -')
        print(f'Your folders: ')
        for folder in course.load_folders():
            print(f"{folder} \n")
        print('--- WHAT TO DO NEXT ---')
        print(' 1. Acces Folder (id)')
        print(' 2. Search question (id)')
        if user.is_admin(course):
            print('--- ADMIN Panel ---')
            print('3. Create folder')
        print(' Press "e" to go back')
        decision = input("Make a choice: ")
        if decision == '1':
            folder_id = int(input("folder id of folder: "))
            with Folder(id=folder_id) as folder:
                folder_view(folder, user)
        elif decision == '2':
            # search_post()
            pass
        elif decision == '3' and user.is_admin(course):
            folder_title = input("Name of folder: ")
            root_folder = int(input("Root folder ID: "))
            course.create_folder(folder_title, root_folder)
        elif decision == 'e':
            break


def search_post(course):
    pass


def folder_view(folder, user):
    while True:
        print(f' — — — — WELCOME {folder.title} — — — -')
        print(f'Your posts: ')
        for thread in folder.load_threads():
            print(f"{thread} \n")
        print('--- WHAT TO DO NEXT ---')
        print(' 1. Acces Thread (id)')
        print(' 2. Create Thread (id)')
        print(' 3. Previous page (id)')
        decision = input("Make a choice: ")
        if decision == '1':
            thread_id = int(input("Thread id of thread: "))
            with Thread(id=thread_id) as thread:
                thread_view(thread, user)
        elif decision == '2':
            thread_title = input("Title of new thread")
            thread_tag = input("Tag of new thread")
            folder.create_thread(user.email, thread_title, thread_tag)
        elif decision == '3':
            break


def thread_view(thread, user):
    while True:
        print(f' — — — — WELCOME {thread.title} — — — -')
        print(f'Your posts: ')
        for post in thread.load_posts():
            print(f"{post} \n")
        print('--- WHAT TO DO NEXT ---')
        print(' 1. Reply post (id)')
        print(' 2. Create post (id)')
        print(' 3. Previous page (id)')
        decision = input("Make a choice: ")
        if decision == '1':
            root_post_id = int(input("Which post: "))
            post_body = input("What body: ")
            thread.create_post(user.email, post_body, root_post_id)
        elif decision == '2':
            post_body = input("What body: ")
            thread.create_post(user.email, post_body)
        elif decision == '3':
            break