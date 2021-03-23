from .connect import Database
from .post import Post

class Thread(Database):
    """Class for thread with methods to insert and query data

    Args:
        Database (Class): Inherits from Database class handling the database connection
    """
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
        """Create post from thread object

        Args:
            user_id (int): user_id of user creating the post
            body (str): text for post content
            root_post_id (int, optional): if post replies to another post. Defaults to None.
            anonymous_post (int, optional): check if post is anonymous. Defaults to 0.
        """
        if root_post_id != None:
            self.execute(
                f"INSERT INTO `post` (`thread_id`,`root_post_id`,`user_id`, `body`, `anonymous_post`) VALUES ({self.id}, {root_post_id}, '{user_id}', '{body}', {anonymous_post})")
        else:
            self.execute(
                f"INSERT INTO `post` (`thread_id`,`user_id`, `body`, `anonymous_post`) VALUES ({self.id}, '{user_id}', '{body}', {anonymous_post})")
        self.commit()

    def load_posts(self):
        """Load all posts in the thread object
        
        Returns:
            list of post objects
        """
        self.execute(f"""
        SELECT post.id, post.thread_id, post.root_post_id, post.user_id, post.body, post.anonymous_post, post.created_at
        FROM post
        INNER JOIN thread ON post.thread_id = thread.id
        WHERE post.thread_id = '{self.id}'
        """)
        posts = self.fetchall()
        return [Post(post[0], post[1], post[2], post[3], post[4], post[5], post[6]) for post in posts]

    def read_thread(self, user_id):
        """insert read into user_reads_thread table

        Args:
            user object for user reading the thread
        """
        self.execute(f"""
        INSERT INTO user_reads_thread (user_id, thread_id) VALUES ('{user_id}', {self.id})
        """)
        self.commit()

    def __str__(self):
        """makes it possile to directly print thread

        Returns:
            str: nicely prints a thread
        """
        return f"Thread ID: {self.id} | Folder ID: {self.folder_id} | User ID: {self.user_id} | Title: {self.title}"