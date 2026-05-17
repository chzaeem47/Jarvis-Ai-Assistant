import csv
import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'notepad', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\notepad')"
# cursor.execute(query)
# con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

query = "INSERT INTO web_command VALUES (null,'portal', 'https://swl-sis.comsats.edu.pk/CourseRegistration/')"
cursor.execute(query)
con.commit()