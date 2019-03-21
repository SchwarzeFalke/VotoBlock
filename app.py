from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response

from vote import Vote

import mysql.connector
import os
load_dotenv()  # Load .env file with the env variables

connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                     host=os.getenv("DB_HOST"),
                                     database=os.getenv("DB_NAME"))
cursor = connection.cursor()

app = Flask(__name__)


@app.route('/')
def index():
    response = make_response(str('Welcome to VotoBlock!'))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

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

# Section: Vote routes
@app.route('/vote', methods=['GET'])
def getVote():
    vote = Vote(connection, cursor)
    voteKey = request.form.get('vote')
    response = make_response(
        str(vote.retrieveVote(voteKey))[2:-1]
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/vote', methods=['POST'])
def postVote():
    vote = Vote(connection, cursor)
    voterKey = request.form.get('voter')
    electionKey = request.form.get('election')
    candidateKey = request.form.get('candidate')
    response = make_response(
        str(vote.generateVote(electionKey, voterKey, candidateKey))
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/election/', methods=['GET'])
def getElectionResults():
    return response


if __name__ == "__main__":
    app.run(port=os.getenv("PORT"), debug=True)
