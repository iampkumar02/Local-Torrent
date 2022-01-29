import mysql.connector as mysql
from dotenv import load_dotenv
import os
import sys

load_dotenv()
try:
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd=os.getenv('password'),
        database="datacamp"
    )
    print("Connected to database...")
except Exception as e:
    print("Database not connected", e)
    sys.exit()

cursor = db.cursor()
# cursor.execute("CREATE DATABASE datacamp")
# cursor.execute("SHOW DATABASES")
# databases = cursor.fetchall()
# for database in databases:
#     print(database)

# cursor.execute(
#     "CREATE TABLE users (username VARCHAR(255), file_dir VARCHAR(255),file_id INT,UNIQUE(file_id))")
# try:
#     cursor.execute(
#         "CREATE TABLE upload_file_list (id INT,file_name TEXT,FOREIGN KEY(id) REFERENCES users(file_id))")
# except Exception as e:

# cursor.execute("SHOW TABLES")

## 'DESC table_name' is used to get all columns information
# cursor.execute("DESC users")

