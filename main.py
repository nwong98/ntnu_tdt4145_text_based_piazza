from classes.connect import Database
from functions import start

drop_all = 'DROP DATABASE db'

with Database() as connection:
    connection.execute_script('sql.txt')

start()

with Database() as connection:
    connection.execute(drop_all)
    print("Dropped")