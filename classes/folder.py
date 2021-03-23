from .connect import Database
from .thread import Thread

class Folder(Database):
    """Class for folder with methods to insert and query data

    Args:
        Database (Class): Inherits from Database class handling the database connection
    """
    def __init__(self, id=None, course_id=None, root_folder_id=None, title=None):
        super().__init__()
        self.id = id
        self.course_id = course_id
        self.root_folder_id = root_folder_id
        self.title = title
        if self.id != None:
            # if folder_id is provided: populate object from database
            self.execute(
                f"SELECT course_id, root_folder_id, title FROM folder WHERE folder.id = '{self.id}'")
            self.course_id, self.root_folder_id, self.title = self.fetchone()

    def create_thread(self, user_id, thread_title, thread_tag):
        """create thread and insert into database

        Args:
            user_id (int): id of user creating the thread
            thread_title (str): title of the thread
            thread_tag (str): tag of the thread
        """
        self.execute(
            f"INSERT INTO `thread` (`folder_id`,`user_id`,`title`, `tag`) VALUES ('{self.id}', '{user_id}', '{thread_title}', '{thread_tag}')")
        self.commit()

    def load_threads(self):
        """Load threads in folder

        Returns:
            list of threads: return threads as objects
        """
        self.execute(f"""
        SELECT thread.id, thread.folder_id, thread.user_id, thread.title, thread.tag, thread.created_at
        FROM thread
        INNER JOIN folder ON thread.folder_id = folder.id
        WHERE thread.folder_id = '{self.id}'
        """)
        threads = self.fetchall()
        return [Thread(thread[0], thread[1], thread[2], thread[3], thread[4], thread[5]) for thread in threads]

    def __str__(self):
        """makes it possile to directly print folder

        Returns:
            str: nicely prints a folder
        """
        return f"Folder ID: {self.id} | Course ID: {self.course_id} | Folder Name: {self.title} | Parent Folder: {self.root_folder_id}"