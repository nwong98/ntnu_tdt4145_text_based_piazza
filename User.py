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
        INNER JOIN participates_in_course ON course.course_id = participates_in_course.course_id
        WHERE participates_in_course.email = '{self.email}'
        """)
        courses = self.fetchall()
        return [Course(course[0], course[1], course[2]) for course in courses]
    
    def add_user_to_course(self, course_id):
        self.execute(f"INSERT INTO `participates_in_course` VALUES ('{self.email}', {course_id})")
        self.commit()

    def add_user_to_viewed(self, thread_id):
        self.execute(f"INSERT INTO `has_read` (`email`, `thread_id`) VALUES ('{self.email}', '{thread_id}')")
        self.commit()

    def add_user_to_liked(self, thread_id):
        self.execute(f"INSERT INTO `user_likes_post` (`email`, `thread_id`) VALUES ('{self.email}', '{thread_id}')")
        self.commit()

class CourseAdmin(User):
    def __init__(self, email = "", password = "", full_name = ""):
        super().__init__(email, password, full_name)

    def create_course(self, course_name, term):
        self.execute(f"INSERT INTO course (`course_name`, `term`) VALUES ('{course_name}', '{term}')")


class Course(Database):
    def __init__(self, course_id=None, course_name=None, term=None):
        self.course_id = course_id
        self.course_name = course_name
        self.course_term = term
        Database.__init__(self)
    
    def __str__(self):
        return f"Course ID: {self.course_id} | Course Name: {self.course_name} | Course Term: {self.course_term}"
    
    def load_course(self):
        self.execute(f"SELECT * FROM course WHERE course.course_id = '{self.course_id}'")
        course = self.fetchone()
        self.course_name = course[1]
        self.course_term = course[2]
        return course

    def create_course(self):
        self.execute(f"INSERT INTO `course` (`course_name`,`term`) VALUES ('{self.course_name}', '{self.course_term}')")
        self.execute(f"SELECT LAST_INSERT_ID()")
        course_id = self.fetchone()[0]
        self.course_id = course_id
    
    def create_folder(self, folder_name, root_folder=None):
        if root_folder != None:
            self.execute(f"INSERT INTO folder (course_id, folder_name, parent_folder) VALUES ('{self.course_id}', '{folder_name}', '{root_folder}')")
        else:
            self.execute(f"INSERT INTO folder (course_id, folder_name) VALUES ('{self.course_id}', '{folder_name}')")

    def load_folders(self):
        self.execute(f"""
        SELECT folder.folder_id, folder.folder_name, folder.course_id, folder.parent_folder
        FROM folder
        INNER JOIN course ON course.course_id = folder.course_id
        WHERE course.course_id = '{self.course_id}'
        """)
        folders = self.fetchall()
        print(folders)
        return [Folder(folder_id = folder[0], folder_name = folder[1], course_id = folder[2], parent_folder = folder[3]) for folder in folders]

class Folder(Database):
    def __init__(self, folder_id=None, folder_name=None, course_id=None, parent_folder=None):
        self.folder_id = folder_id
        self.course_id = course_id
        self.folder_name = folder_name
        self.parent_folder = parent_folder
        Database.__init__(self)

    def load_folder(self):
        self.execute(f"SELECT * FROM folder WHERE folder.folder_id = '{self.folder_id}'")
        folder = self.fetchone()
        self.course_id = folder[1]
        self.folder_name = folder[2]
        self.parent_folder = folder[3]
        return folder

    def create_thread(self):
        self.execute("""
        SELECT 1
        """)

    def load_threads(self) -> list[Thread]:
        self.execute("""
        SELECT 1
        """)
    
    def __str__(self):
        return f"Folder ID: {self.folder_id} | Course ID: {self.course_id} | Folder Name: {self.folder_name} | Parent Folder: {self.parent_folder}"

# class Thread(Database):
#     def __init__(self, thread_id="", folder_id="", email="", title="", color_status='RED', created_at=""):
#         self.thread_id = thread_id
#         self.folder_id = folder_id
#         self.email = email
#         self.title = title
#         self.color_status = color_status
#         self.created_at = created_at
#         Database.__init__(self)
    
#     def load_posts(self) -> list[Post]:
#         self.execute("""
#         SELECT 1
#         """)

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