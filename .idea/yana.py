from mysql.connector import connect
from pprint import pprint as print
db = connect(user = 'root', host = 'localhost', password = 'begzod', database='learning_center')

if db.is_connected:
    cursor = db.cursor()
    cursor.execute("select distinct * from course")
    