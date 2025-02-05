from datetime import datetime
import mysql.connector
import csv



db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "bahodir",
    database = "learning_center"
)
buyruq = db.cursor()



bugun = datetime.today().strftime('%Y-%m-%d')

buyruq.execute("select * from users")
all_users = buyruq.fetchall()
for user in all_users:
    print(user)

with open('all_users.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "full_name","phone", "datetime","username","t_id","course_id","branch_id"]) 
    for user in all_users:
        writer.writerow(user)
buyruq.execute("select * from users where datetime=%s",(bugun,))
today_users = buyruq.fetchall()
for user in today_users:
    print(user)

with open('users_today.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "full_name","phone", "datetime","username","t_id","course_id","branch_id"]) 
    for user in today_users:
        writer.writerow(user)