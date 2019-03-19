# @Author: schwarze_falke
# @Date:   2019-02-21T00:51:54-06:00
# @Last modified by:   schwarze_falke
# @Last modified time: 2019-02-21T01:05:19-06:00

from flask import Flask, request, jsonify, make_response

import MySQLdb
import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file with the env variables

app = Flask(__name__)


@app.route('/')
def index():
    db = MySQLdb.connect(host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"),
                         passwd=os.getenv("DB_PASS"), db=os.getenv("DB_NAME"))
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    for row in cursor.fetchall():
        print(row[0])
    db.close()
    return 'Welcome to VoteBlock!'


@app.route('/login/', methods=['GET'])
def login():
    return response


@app.route('/signup/', methods=['POST'])
def login():
    return response


@app.route('/candidate/', methods=['POST'])
def login():
    return response


@app.route('/candidate/', methods=['DELETE'])
def login():
    return response


@app.route('/vote/', methods=['POST'])
def login():
    return response


if __name__ == "__main__":
    app.run()
