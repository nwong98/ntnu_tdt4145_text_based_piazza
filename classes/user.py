from .connect import Database
from .course import Course

class User(Database):
    """Class for user with methods to insert and query data

    Args:
        Database (Class): Inherits from Database class handling the database connection
    """
    def __init__(self, email=None, password=None, full_name=None):
        super().__init__()
        self.email = email
        self.password = password
        self.full_name = full_name

    def create_user(self):
        """Method to insert user into database"""
        self.execute(
            f"INSERT INTO `user` (`email`,`pass`,`full_name`) VALUES ('{self.email}', '{self.password}', '{self.full_name}')")
        self.commit()

    def validate_user(self):
        """Check if email and password matches any tuples in database

        Returns:
            Boolean: if user is in database
        """
        self.execute(
            f"SELECT * FROM user WHERE user.email = '{self.email}' AND user.pass = '{self.password}'")
        if self.fetchone() != None:
            return True
        else:
            return False

    def load_courses(self):
        """Load courses user is in

        Returns:
            Course: return course objects
        """
        self.execute(f"""
        SELECT *
        FROM course
        INNER JOIN user_in_course ON course.id = user_in_course.course_id
        WHERE user_in_course.user_id = '{self.email}'
        """)
        courses = self.fetchall()
        return [Course(course[0], course[1], course[2]) for course in courses]
    
    def load_all_courses(self):
        """Load all courses in database

        Returns:
            Course: return course objects
        """
        self.execute(f"""
        SELECT *
        FROM course
        """)
        courses = self.fetchall()
        return [Course(course[0], course[1], course[2]) for course in courses]

    def add_user_to_course(self, course_id, user_type='Student'):
        """Add user to course

        Args:
            course_id (int): id of course user wants to be added to
            user_type (str, optional): Define what type of user to be added. Defaults to 'Student'.
        """
        self.execute(
            f"INSERT INTO `user_in_course` VALUES ('{self.email}', {course_id}, '{user_type}')")
        self.commit()

    def add_user_to_viewed(self, thread_id):
        """Insert user to user_has_read table

        Args:
            thread_id (int): id of thread user has viewed
        """
        self.execute(
            f"INSERT INTO `user_has_read` (`user_id`, `thread_id`) VALUES ('{self.email}', '{thread_id}')")
        self.commit()

    def add_user_to_liked(self, post_id):
        """Insert user to user_likes post table

        Args:
            post_id (int): id of post user has liked
        """
        self.execute(
            f"INSERT INTO `user_likes_post` (`user_id`, `post_id`) VALUES ('{self.email}', '{post_id}')")
        self.commit()
    
    def is_admin(self, course_id):
        """Check if user id admin in course
        Args:
            course_id: id of course to check
        Returns:
            Boolean: return if user is admin in course
        """
        self.execute(f"""
        SELECT *
        FROM user_in_course
        WHERE user_in_course.user_id = '{self.email}' AND user_in_course.course_id = {course_id} AND user_in_course.user_type = 'Admin'
        """)
        if self.fetchone() != None:
            return True
        else:
            return False