from Connect import Database

class User(Database):

    def __init__(self, email = None, password = None, full_name = None):
        super().__init__()
        self.email = email
        self.password = password
        self.full_name = full_name

    def create_user(self):
        self.execute(f"INSERT INTO `user` (`email`,`pass`,`full_name`) VALUES ('{self.email}', '{self.password}', '{self.full_name}')")

    def validate_user(self):
        self.execute(f"SELECT * FROM user WHERE user.email = '{self.email}' AND user.pass = '{self.password}'")
        if self.fetchone() != None:
            return True
        else:
            return False
    
    def load_user(self):
        self.execute(f"SELECT * FROM user WHERE user.email = '{self.email}'")
        return self.fetchone()
    
    def load_courses(self):
        self.execute(f"""
        SELECT *
        FROM course
        INNER JOIN user_in_course ON course.id = user_in_course.course_id
        WHERE user_in_course.user_id = '{self.email}'
        """)
        courses = self.fetchall()
        return [Course(course[0], course[1], course[2]) for course in courses]
    
    def add_user_to_course(self, course_id, user_type='Student'):
        self.execute(f"INSERT INTO `user_in_course` VALUES ('{self.email}', {course_id}, '{user_type}')")
        self.commit()

    def add_user_to_viewed(self, thread_id):
        self.execute(f"INSERT INTO `user_has_read` (`user_id`, `thread_id`) VALUES ('{self.email}', '{thread_id}')")
        self.commit()

    def add_user_to_liked(self, post_id):
        self.execute(f"INSERT INTO `user_likes_post` (`user_id`, `post_id`) VALUES ('{self.email}', '{post_id}')")
        self.commit()

class CourseAdmin(User):
    def __init__(self, email = "", password = "", full_name = ""):
        super().__init__(email, password, full_name)

    def create_course(self, course_name, term):
        self.execute(f"INSERT INTO course (`title`, `term`) VALUES ('{course_name}', '{term}')")


class Course(Database):
    def __init__(self, id=None, title=None, term=None):
        self.id = id
        self.title = title
        self.term = term
        Database.__init__(self)
    
    def __str__(self):
        return f"Course ID: {self.id} | Course Name: {self.title} | Course Term: {self.term}"
    
    def load_course(self):
        self.execute(f"SELECT * FROM course WHERE course.id = '{self.id}'")
        course = self.fetchone()
        self.title = course[1]
        self.term = course[2]
        return course

    def create_course(self):
        self.execute(f"INSERT INTO `course` (`title`,`term`) VALUES ('{self.title}', '{self.term}')")
        self.execute(f"SELECT LAST_INSERT_ID()")
        course_id = self.fetchone()[0]
        self.id = course_id
    
    def create_folder(self, title, root_folder_id=None):
        if root_folder_id != None:
            self.execute(f"INSERT INTO folder (course_id, title, root_folder_id) VALUES ('{self.course_id}', '{title}', '{root_folder_id}')")
        else:
            self.execute(f"INSERT INTO folder (course_id, title) VALUES ('{self.course_id}', '{title}')")

    def load_folders(self):
        self.execute(f"""
        SELECT folder.id, folder.course_id, folder.root_folder_id, folder.title
        FROM folder
        INNER JOIN course ON course.id = folder.course_id
        WHERE course.id = '{self.id}'
        """)
        folders = self.fetchall()
        return [Folder(folder[0],folder[1], folder[2], folder[3]) for folder in folders]

class Folder(Database):
    def __init__(self, id=None, course_id=None, root_folder_id=None, title=None):
        self.id = id
        self.course_id = course_id
        self.root_folder_id = root_folder_id
        self.title = title
        Database.__init__(self)

    def load_folder(self):
        self.execute(f"SELECT course_id, root_folder_id, title FROM folder WHERE folder.id = '{self.id}'")
        folder = self.fetchone()
        self.course_id = folder[0]
        self.root_folder_id = folder[1]
        self.title = folder[2]
        return folder

    def create_thread(self):
        self.execute("""
        SELECT 1
        """)

    def load_threads(self):
        self.execute(f"""
        SELECT thread.id, thread.folder_id, thread.user_id, thread.title, thread.tag, thread.created_at
        FROM thread
        INNER JOIN folder ON thread.folder_id = folder.id
        WHERE thread.folder_id = '{self.id}'
        """)
        threads = self.fetchall()
        return [Thread(thread[0],thread[1], thread[2], thread[3], thread[4], thread[5]) for thread in threads]
    
    def __str__(self):
        return f"Folder ID: {self.id} | Course ID: {self.course_id} | Folder Name: {self.title} | Parent Folder: {self.root_folder_id}"

class Thread(Database):
    def __init__(self, id=None, folder_id=None, user_id=None, title=None, tag=None, created_at=None):
        self.id = id
        self.folder_id = folder_id
        self.user_id = user_id
        self.title = title
        self.tag = tag
        self.created_at = created_at
        Database.__init__(self)
    
    def load_posts(self):
        self.execute("""
        SELECT 1
        """)

    def __str__(self):
        return f"Thread ID: {self.id} | Folder ID: {self.folder_id} | User ID: {self.user_id} | Title: {self.title}"

# class Post(Database):
#     def __init__(self, post_id="", root_post="", folder_id="", email="", title="", body="", anonymous_post=0, created_at=""):
#         self.post_id = post_id
#         self.parent_post = parent_post
#         self.email = email
#         self.title = title
#         self.content = content
#         self.create_time = None
#         self.anonymous_post = anonymous_post
#         Database.__init__(self)
    
#     def create_posts(self):
#         self.execute("""
#         SELECT 1
#         """)

#     def load_posts(self):
#         self.execute("""
#         SELECT 1
#         """)