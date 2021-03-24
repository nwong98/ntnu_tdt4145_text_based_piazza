from classes.user import User
from classes.course import Course
from classes.folder import Folder
from classes.thread import Thread
from classes.post import Post

def start():
    """Home screen of program (Piazza)
    - Possible for users to register a profile
    - Possible for users to log in
    - Possible for users to exit the program
    """
    while True:
        print(' — — — — MENU — — — -')
        print(' 1. Register')
        print(' 2. Login')
        print(' 3. Exit') # This will also drop the database
        print(' — — — — — — — — — — ')
        decision = input("Choose an option: ")
        print(' — — — — — — — — — — \n')
        if decision == '1':
            register_user()
        elif decision == '2':
            print(' — — — User Login — — —')
            user_email = input('Enter email : ')
            user_password = input('Enter password : ')
            print(' — — — — — — — — — — \n')
            with User(email=user_email, password=user_password) as user:
                if user.validate_user() == True:
                    login_user(user)
                else:
                    print(' — — — — INVALID CREDENTIALS — — — — \n')
        elif decision == '3':
            break


def register_user():
    """User registration
    - User registration by creating a User object based on input values
    - Upon registration, user is automatically directed to the login_user function
    """
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
    """User is logged into the program
    - User can access a course they are registered in
    - User can register in availanle courses in the database
    - User can create a new course

    Args:
        user (User class): user class initiated from earlier
    """
    while True:
        print(f' — — — — WELCOME {user.email} — — — -')
        print(f"Courses you're registered in: \n")
        for course in user.load_courses():
            print(f"{course}") # load courses user is registered in from before
        print(' — — — — — — — — — — \n')
        print('--- AVAILABLE OPTIONS ---')
        print(' 1. Acces Course')
        print(' 2. Register in course')
        print(' 3. Create Course')
        print(' 4. Previous page')
        print(' — — — — — — — — — — ')
        decision = input("Choose an option: ")
        print(' — — — — — — — — — — \n')
        if decision == '1':
            course_id = int(input("Course id of course: "))
                # Check if entered course id raises any errors
            with Course(id=course_id) as course:
                course_view(course, user)
            print("The course you entered does not exist.\n")
        elif decision == '2':
            for course in user.load_all_courses():
                print(f"{course} \n") # loads and prints all courses available in a formatted view.
            course_id = int(input("Course id of course: "))
            try:
                # Check if desired course exist in database.
                user.add_user_to_course(course_id)
            except:
                print("The course you entered does not exist.\n")
        elif decision == '3':
            # creates course and automatically adds user to course as admin
            course_title = input("Name of course: ")
            course_term = input("Term of course: ")
            with Course(title=course_title, term=course_term) as course:
                course.create_course()
            print(course.id)
            user.add_user_to_course(course.id, user_type='Admin')
        elif decision == '4':
            break


def course_view(course, user):
    """View within a specific course
    - User can access folder in course
    - User can search for questions within the course
    - Admin can create folder
    - Admin can view statistics of course
    - User/Admin can return to previous view
    Args:
        course (Course class): course class initiated from earlier
        user (User class): user class inititated from earlier
    """
    while True:
        print(f' — — — — WELCOME {course.title} — — — -')
        print(f'Your folders: \n')
        for folder in course.load_folders():
            print(f"{folder}")
        print(' — — — — — — — — — — \n')
        print('--- AVAILABLE OPTIONS ---')
        print(' 1. Acces Folder (id)')
        print(' 2. Search question (id)')
        if user.is_admin(course.id):
            print('--- ADMIN Panel ---')
            print('3. Create folder')
            print('4. View Statistics')
        print('5. Previous page')
        print(' — — — — — — — — — — ')
        decision = input("Choose an option: ")
        print(' — — — — — — — — — — ')
        if decision == '1':
            try:
                folder_id = int(input("folder id of folder: "))
                with Folder(id=folder_id) as folder:
                    folder_view(folder, user)
            except:
                print("The folder does not exist.")
        elif decision == '2':
            text = input("What to search: ")
            print(course.search_text(text))
        elif decision == '3' and user.is_admin(course.id):
            folder_title = input("Name of folder: ")
            root_folder = int(input("Root folder ID: "))
            course.create_folder(title=folder_title, root_folder_id=root_folder)
        elif decision == '4' and user.is_admin(course.id):
            print(f'--- STATISTICS FOR {course.title} ---')
            print(f"Total users in course: {course.load_total_users()} users")
            print(f"Total threads in course: {course.load_total_threads()} threads")
            print(f"Total posts in course: {course.load_total_posts()} posts")
            print(f"    -Total posts by instructors: {course.load_total_instructor_responses()} instructor responses")
            print(f"    -Total posts by students: {course.load_total_student_responses()} student responses")
        elif decision == '5':
            break

def folder_view(folder, user):
    """View within a folder
    - User can access threads within the folder they're in.
    - User can create a new thread
    - User can go back to previous view
    Args:
        folder (Folder class): Previous initiated folder
        user (User class): previous initiated user
    """
    while True:
        print(f' — — — — WELCOME {folder.title} — — — -')
        print(f'Threads in folder: ')
        for thread in folder.load_threads():
            print(f"{thread} \n")
        print('--- AVAILABLE OPTIONS ---')
        print(' 1. Acces Thread')
        print(' 2. Create Thread')
        print(' 3. Previous page')
        decision = input("Choose an option: \n")
        if decision == '1':
            try:
                # check if thread us accessible
                thread_id = int(input("Id of thread: "))
                with Thread(id=thread_id) as thread:
                    try:
                        thread.read_thread(user_id=user.email) #check if user has already read thread
                    except:
                        print("View already registered. ") # user view is only registered once
                    thread_view(thread, user)
            except:
                print("INVALID")
        elif decision == '2':
            thread_title = input("Title of new thread: ")
            thread_tag = input("Tag of new thread: ")
            folder.create_thread(user.email, thread_title, thread_tag)
        elif decision == '3':
            break


def thread_view(thread, user):
    """View within a thread
    - User can reply to a post in the thread
    - User can create a new post in the thread
    - User can like a given post in the thread
    - User can go back to previous view
    Args:
        thread (Thread class): initiated from previous view
        user (User class): inititaed from previous view
    """
    while True:
        print(f' — — — — WELCOME {thread.title} — — — -')
        for post in thread.load_posts():
            print(f"{post} \n")
        print('--- AVAILABLE OPTIONS ---')
        print(' 1. Reply post')
        print(' 2. Create post')
        print(' 3. Like post')
        print(' 4. Previous page')
        decision = input("Make a choice: ")
        if decision == '1':
            root_post_id = int(input("Id of post you want to reply to: "))
            post_body = input("Reply message: ")
            anonymous_post = int(input("Do you want the post to be posted anonymously (1/0): ")) # if anonymous, user email and name will be hidden
            thread.create_post(user.email, post_body, root_post_id, anonymous_post=anonymous_post)
        elif decision == '2':
            post_body = input("Post message: ")
            thread.create_post(user.email, post_body)
        elif decision == '3':
            post_id = int(input("Id of post you want to like: "))
            with Post(id=post_id) as post:
                try:
                    post.likes_post(user.email)
                    print("Post liked!")
                except:
                    print("You've already liked this post...")
        elif decision == '4':
            break