# @Author: schwarze_falke
# @Date:   2019-02-21T00:51:54-06:00
# @Last modified by:   schwarze_falke
# @Last modified time: 2019-02-21T01:05:19-06:00
import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file with the env variables

db = MySQLdb.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"),
                     passwd=os.getenv("DB_PASS"), db=os.getenv("DB_NAME"))
cursor = db.cursor()
cursor.execute("SHOW TABLES")
for row in cursor.fetchall():
    print(row[0])
db.close()
