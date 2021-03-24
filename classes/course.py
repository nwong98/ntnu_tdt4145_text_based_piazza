from .connect import Database
from .folder import Folder

class Course(Database):
    """Class for course with methods to insert and query data

    Args:
        Database (Class): Inherits from Database class handling the database connection
    """
    def __init__(self, id=None, title=None, term=None):
        super().__init__()
        self.id = id
        self.title = title
        self.term = term
        if self.id != None:
            # if course_id is provided: populate object from database
            self.execute(
                f"SELECT title, term FROM course WHERE course.id = '{self.id}'")
            self.title, self.term = self.fetchone()

    def __str__(self):
        return f"Course ID: {self.id} | Course Name: {self.title} | Course Term: {self.term}"

    def create_course(self):
        """Insert course into database"""
        self.execute(
            f"INSERT INTO `course` (`title`,`term`) VALUES ('{self.title}', '{self.term}')")
        self.execute(f"SELECT LAST_INSERT_ID()")
        course_id = self.fetchone()[0]
        self.id = course_id

    def create_folder(self, title, root_folder_id=None):
        """Create folder and insert it into folder table

        Args:
            title (str): title of folder
            root_folder_id (int, optional): If folder is nested under another folder. Defaults to None.
        """
        if root_folder_id != None:
            self.execute(
                f"INSERT INTO folder (course_id, title, root_folder_id) VALUES ({self.id}, '{title}', {root_folder_id})")
        else:
            self.execute(
                f"INSERT INTO folder (course_id, title) VALUES ({self.id}, '{title}')")
        self.commit()

    def load_folders(self):
        """Load folders in course

        Returns:
            List of folders: return folder objects
        """
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
            SELECT thread.*
            FROM folder
            INNER JOIN thread ON folder.id = thread.folder_id
            INNER JOIN post ON thread.id = post.thread_id
            WHERE folder.course_id = '{self.id}' AND thread.title LIKE '%{string}%' OR post.body LIKE '%{string}%'
            """)
        threads = self.fetchall()
        for thread in threads:
            print(thread)
    
    def load_total_users(self):
        """load user statistics (number of users in course)

        Returns:
            int: number of users in course
        """
        self.execute(
            f"""
            SELECT COUNT(user_id)
            FROM user_in_course
            WHERE course_id = {self.id};
            """)
        return self.fetchone()[0]

    def load_total_threads(self):
        """load thread statistics (number of threads in course)

        Returns:
            int: number of threads in course
        """
        self.execute(
            f"""
            SELECT COUNT(thread.id)
            FROM folder
            JOIN thread on folder.id = thread.folder_id
            WHERE course_id={self.id};
            """)
        return self.fetchone()[0]
    
    def load_total_posts(self):
        """load post statistics (number of posts in course)

        Returns:
            int: number of posts in course
        """
        self.execute(
            f"""
            SELECT COUNT(post.id)
            FROM folder
            JOIN thread on folder.id = thread.folder_id
            JOIN post on thread.id = post.thread_id
            WHERE folder.course_id = '{self.id}';
            """)
        return self.fetchone()[0]

    def load_total_instructor_responses(self):
        """load total instructor answer statistics

        Returns:
            int: number of posts made by instructors
        """
        self.execute(
            f"""
            SELECT COUNT(post.id)
            FROM course
            JOIN folder ON course.id = folder.course_id
            JOIN thread ON folder.id = thread.folder_id
            JOIN post ON thread.id = post.thread_id
            JOIN user_in_course ON post.user_id = user_in_course.user_id
            WHERE course.id = {self.id} AND user_in_course.user_type = 'Admin' OR user_in_course.user_type= 'Instructor';
            """
        )
        return self.fetchone()[0]

    def load_total_student_responses(self):
        """load total student answer statistics

        Returns:
            int: number of posts made by students
        """
        self.execute(
            f"""
            SELECT COUNT(post.id)
            FROM course
            JOIN folder ON course.id = folder.course_id
            JOIN thread ON folder.id = thread.folder_id
            JOIN post ON thread.id = post.thread_id
            JOIN user_in_course ON post.user_id = user_in_course.user_id
            WHERE course.id = {self.id} AND user_in_course.user_type = 'Student';
            """
        )
        return self.fetchone()[0] 