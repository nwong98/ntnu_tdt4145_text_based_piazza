from Connect import Database


class User(Database):

    def __init__(self, email=None, password=None, full_name=None):
        super().__init__()
        self.email = email
        self.password = password
        self.full_name = full_name
        # if self.email != None:
        #     self.execute(
        #         f"SELECT pass, full_name FROM user WHERE user.email = '{self.email}'")
        #     self.password, self.full_name = self.fetchone()

    def create_user(self):
        self.execute(
            f"INSERT INTO `user` (`email`,`pass`,`full_name`) VALUES ('{self.email}', '{self.password}', '{self.full_name}')")
        self.commit()

    def validate_user(self):
        self.execute(
            f"SELECT * FROM user WHERE user.email = '{self.email}' AND user.pass = '{self.password}'")
        if self.fetchone() != None:
            return True
        else:
            return False

    def load_courses(self):
        self.execute(f"""
        SELECT *
        FROM course
        INNER JOIN user_in_course ON course.id = user_in_course.course_id
        WHERE user_in_course.user_id = '{self.email}'
        """)
        courses = self.fetchall()
        return [Course(course[0], course[1], course[2]) for course in courses]
    
    def load_all_courses(self):
        self.execute(f"""
        SELECT *
        FROM course
        """)
        courses = self.fetchall()
        return [Course(course[0], course[1], course[2]) for course in courses]

    def add_user_to_course(self, course_id, user_type='Student'):
        self.execute(
            f"INSERT INTO `user_in_course` VALUES ('{self.email}', {course_id}, '{user_type}')")
        self.commit()

    def add_user_to_viewed(self, thread_id):
        self.execute(
            f"INSERT INTO `user_has_read` (`user_id`, `thread_id`) VALUES ('{self.email}', '{thread_id}')")
        self.commit()

    def add_user_to_liked(self, post_id):
        self.execute(
            f"INSERT INTO `user_likes_post` (`user_id`, `post_id`) VALUES ('{self.email}', '{post_id}')")
        self.commit()
    
    def is_admin(self, course):
        self.execute(f"""
        SELECT *
        FROM user_in_course
        WHERE user_in_course.user_id = '{self.email}' AND user_in_course.user_type = 'Admin'
        """)
        if self.fetchone() != None:
            return True
        else:
            return False

class Course(Database):
    def __init__(self, id=None, title=None, term=None):
        super().__init__()
        self.id = id
        self.title = title
        self.term = term
        if self.id != None:
            self.execute(
                f"SELECT title, term FROM course WHERE course.id = '{self.id}'")
            self.title, self.term = self.fetchone()

    def __str__(self):
        return f"Course ID: {self.id} | Course Name: {self.title} | Course Term: {self.term}"

    def create_course(self):
        self.execute(
            f"INSERT INTO `course` (`title`,`term`) VALUES ('{self.title}', '{self.term}')")
        self.execute(f"SELECT LAST_INSERT_ID()")
        course_id = self.fetchone()[0]
        self.id = course_id

    def create_folder(self, title, root_folder_id=None):
        if root_folder_id != None:
            self.execute(
                f"INSERT INTO folder (course_id, title, root_folder_id) VALUES ('{self.course_id}', '{title}', '{root_folder_id}')")
        else:
            self.execute(
                f"INSERT INTO folder (course_id, title) VALUES ('{self.course_id}', '{title}')")
        self.commit()

    def load_folders(self):
        self.execute(f"""
        SELECT folder.id, folder.course_id, folder.root_folder_id, folder.title
        FROM folder
        INNER JOIN course ON course.id = folder.course_id
        WHERE course.id = '{self.id}'
        """)
        folders = self.fetchall()
        return [Folder(folder[0], folder[1], folder[2], folder[3]) for folder in folders]

    def search_text(self, string):
        self.execute(f"""
        SELECT thread.title, post.body
        FROM folder INNER JOIN thread ON folder.id = thread.folder_id
        INNER JOIN post ON thread.id = post.thread_id
        WHERE folder.course_id = '{self.id}' AND thread.title LIKE '%{string}%' OR post.body LIKE '%{string}%'
        """)
        return self.fetchall()
    
    def load_total_posts(self):
        self.execute(
            f"""
            SELECT COUNT(user_id)
            FROM user_in_course
            WHERE course_id='{self.id}'
            """)
        return self.fetchone()

    def load_total_users(self):
        self.execute(
            f"""
            SELECT COUNT(post.id)
            FROM folder
            JOIN thread on folder.id = thread.folder_id
            JOIN post on thread.id = post.thread_id
            WHERE folder.course_id = {self.id};
            """)
        return self.fetchone()

    def load_total_threads(self):
        self.execute(
            f"""
            SELECT COUNT(post.id)
            FROM folder
            JOIN thread on folder.id = thread.folder_id
            JOIN post on thread.id = post.thread_id
            WHERE folder.course_id = '{self.id}';
            """)
        return self.fetchone()

    def load_total_threads(self):
        self.execute(
            f"""
            SELECT  COUNT(thread.id)
            FROM folder
            JOIN thread on folder.id = thread.folder_id
            WHERE course_id={self.id};
            """)
        return self.fetchone()

    def load_total_instructor_responses(self):
        pass

    def load_total_student_responses(self):
        pass

class Folder(Database):
    def __init__(self, id=None, course_id=None, root_folder_id=None, title=None):
        super().__init__()
        self.id = id
        self.course_id = course_id
        self.root_folder_id = root_folder_id
        self.title = title
        if self.id != None:
            self.execute(
                f"SELECT course_id, root_folder_id, title FROM folder WHERE folder.id = '{self.id}'")
            self.course_id, self.root_folder_id, self.title = self.fetchone()

    def create_thread(self, user_id, thread_title, thread_tag):
        self.execute(
            f"INSERT INTO `thread` (`folder_id`,`user_id`,`title`, `tag`) VALUES ('{self.id}', '{user_id}', '{thread_title}', '{thread_tag}')")
        self.commit()

    def load_threads(self):
        self.execute(f"""
        SELECT thread.id, thread.folder_id, thread.user_id, thread.title, thread.tag, thread.created_at
        FROM thread
        INNER JOIN folder ON thread.folder_id = folder.id
        WHERE thread.folder_id = '{self.id}'
        """)
        threads = self.fetchall()
        return [Thread(thread[0], thread[1], thread[2], thread[3], thread[4], thread[5]) for thread in threads]

    def __str__(self):
        return f"Folder ID: {self.id} | Course ID: {self.course_id} | Folder Name: {self.title} | Parent Folder: {self.root_folder_id}"


class Thread(Database):
    def __init__(self, id=None, folder_id=None, user_id=None, title=None, tag=None, created_at=None):
        super().__init__()
        self.id = id
        self.folder_id = folder_id
        self.user_id = user_id
        self.title = title
        self.tag = tag
        self.created_at = created_at
        if self.id != None:
            self.execute(
                f"SELECT folder_id, user_id, title, tag, created_at FROM thread WHERE thread.id = '{self.id}'")
            self.folder_id, self.user_id, self.title, self.tag, self.created_at = self.fetchone()

    def create_post(self, user_id, body, root_post_id=None, anonymous_post=0):
        if root_post_id != None:
            self.execute(
                f"INSERT INTO `post` (`thread_id`,`root_post_id`,`user_id`, `body`, `anonymous_post`) VALUES ({self.id}, {root_post_id}, '{user_id}', '{body}', {anonymous_post})")
        else:
            self.execute(
                f"INSERT INTO `post` (`thread_id`,`user_id`, `body`, `anonymous_post`) VALUES ({self.id}, '{user_id}', '{body}', {anonymous_post})")
        self.commit()

    def load_posts(self):
        self.execute(f"""
        SELECT post.id, post.thread_id, post.root_post_id, post.user_id, post.body, post.anonymous_post, post.created_at
        FROM post
        INNER JOIN thread ON post.thread_id = thread.id
        WHERE post.thread_id = '{self.id}'
        """)
        posts = self.fetchall()
        return [Post(post[0], post[1], post[2], post[3], post[4], post[5], post[6]) for post in posts]

    def __str__(self):
        return f"Thread ID: {self.id} | Folder ID: {self.folder_id} | User ID: {self.user_id} | Title: {self.title}"


class Post(Database):
    def __init__(self, id=None, thread_id=None, root_post_id=None, user_id=None, body=None, anonymous_post=0, create_time=None):
        super().__init__()
        self.id = id
        self.thread_id = thread_id
        self.root_post_id = root_post_id
        self.user_id = user_id
        self.body = body
        self.anonymous_post = anonymous_post
        self.create_time = None
        if self.id != None:
            self.execute(
                f"SELECT thread_id, root_post_id, user_id, body, anonymous_post, created_at FROM post WHERE post.id = '{self.id}'")
            self.thread_id, self.root_post_id, self.user_id, self.body, self.anonymous_post, self.created_at = self.fetchone()
        

    def __str__(self):
        return f"Post ID: {self.id} | Thread ID: {self.thread_id} | Root Post ID: {self.root_post_id} | User ID: {self.user_id} | Body: {self.body} | Anonymous Post: {self.anonymous_post} | Create Time: {self.created_at}"
