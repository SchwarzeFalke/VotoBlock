from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv

import mysql.connector
import os
load_dotenv()  # Load .env file with the env variables

app = Flask(__name__)


@app.route('/')
def index():
    db = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                 host=os.getenv("DB_HOST"),
                                 database=os.getenv("DB_NAME"))
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    for row in cursor.fetchall():
        print(row[0])
    db.close()
    return 'Welcome to VoteBlock!'


# @app.route('/login/', methods=['GET'])
# def login():
#    return response


# @app.route('/signup/', methods=['POST'])
# def login():
#    return response


# @app.route('/candidate/', methods=['POST'])
# def login():
#    return response


# @app.route('/candidate/', methods=['DELETE'])
# def login():
#    return response


@app.route('/vote', methods=['GET', 'POST'])
def generateVote():
    param = request.args.get('username')
    print(param)
    return param


@app.route('/election/', methods=['GET'])
def getElectionResults():

    return response


if __name__ == "__main__":
    app.run()
