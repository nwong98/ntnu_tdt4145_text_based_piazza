from .connect import Database
class Post(Database):
    """Class for post with methods to insert and query data

    Args:
        Database (Class): Inherits from Database class handling the database connection
    """
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
            # if post_id is provided: populate object from database
            self.execute(
                f"SELECT thread_id, root_post_id, user_id, body, anonymous_post, created_at FROM post WHERE post.id = '{self.id}'")
            self.thread_id, self.root_post_id, self.user_id, self.body, self.anonymous_post, self.created_at = self.fetchone()
    
    def likes_post(self, user_id):
        """insert read into user_likes_post table

        Args:
            user object for user likes the post
        """
        self.execute(f"""
        INSERT INTO user_likes_post (user_id, post_id) VALUES ('{user_id}', {self.id})
        """)
        self.commit()
    
    @property
    def user_role(self):
        self.execute(f"""
            SELECT user_in_course.user_type
            FROM course
            JOIN folder ON course.id = folder.course_id
            JOIN thread ON folder.id = thread.folder_id 
            JOIN post ON thread.id = post.thread_id
            JOIN user_in_course ON post.user_id = user_in_course.user_id
            WHERE post.id = {self.id};
        """)
        return self.fetchone()[0]
    
    @property
    def post_likes(self):
        self.execute(f"""
            SELECT COUNT(*)
            FROM user_likes_post
            WHERE user_likes_post.post_id = {self.id};
        """)
        return self.fetchone()[0]
        
    def __str__(self):
        """makes it possile to directly print post

        Returns:
            str: nicely prints a post
        """
        if self.anonymous_post == 1:
            return f"Post ID: {self.id} | Thread ID: {self.thread_id} | Root Post ID: {self.root_post_id} | User ID: Anonymous | Body: {self.body} | Create Time: {self.created_at} | {self.user_role} | Likes: {self.post_likes}"
        return f"Post ID: {self.id} | Thread ID: {self.thread_id} | Root Post ID: {self.root_post_id} | User ID: {self.user_id} | Body: {self.body} | Create Time: {self.created_at} | {self.user_role} | Likes: {self.post_likes}"
        