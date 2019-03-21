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

@app.route('/verify/elections/', methods=['GET'])
def verifyElectionPeriod():
    db = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                 host=os.getenv("DB_HOST"),
                                 database=os.getenv("DB_NAME"))

    cursor = db.cursor()
    cursor.execute("SELECT _id, descript FROM election")
    elections = cursor.fetchall()
    return jsonify(elections)


@app.route('/verify/candidates/', methods=['GET'])
def verifyAvailableCandidates():
    db = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                 host=os.getenv("DB_HOST"),
                                 database=os.getenv("DB_NAME"))

    cursor = db.cursor()
    electionId = request.args.get('election_id')
    cursor.execute("SELECT electoral_key, name, middle_name, mlastname, flastname FROM candidate WHERE election_id = '{}'".format(electionId))
    candidates = cursor.fetchall()
    return jsonify(candidates)


@app.route('/candidate/information/', methods=['GET'])
def getCandidateInformation():
    db = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                 host=os.getenv("DB_HOST"),
                                 database=os.getenv("DB_NAME"))

    cursor = db.cursor()
    electoral_key = request.args.get('electoral_key')
    print(electoral_key)
    cursor.execute("SELECT * FROM candidate WHERE electoral_key = '{}'".format(electoral_key))
    candidate = cursor.fetchall()
    return jsonify(candidate)



# @app.route('/login/', methods=['GET'])
# def login():
#    return response


# @app.route('/signup/', methods=['POST'])
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
