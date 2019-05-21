from dotenv import load_dotenv
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

from vote import Vote
from access import Access
from fake_data import Fakerism

import mysql.connector
import os
import json

load_dotenv()  # Load .env file with the env variables

connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                     host=os.getenv("DB_HOST"),
                                     database=os.getenv("DB_NAME"))
cursor = connection.cursor()

app = Flask(__name__)
cors = CORS(app)


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


@app.route('/election/', methods=['GET'])
def getElectionResults():
    db = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                 host=os.getenv("DB_HOST"),
                                 database=os.getenv("DB_NAME"))
    cursor = db.cursor()
    electionid = request.args.get('electionid')
    cursor.execute(
        "SELECT * FROM election WHERE _id = '{}'".format(electionid))
    elections = cursor.fetchall()
    electionDictionary = {}
    lista = []
    return jsonify(elections)


@app.route('/verify/candidates/', methods=['GET'])
def verifyAvailableCandidates():
    db = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                 host=os.getenv("DB_HOST"),
                                 database=os.getenv("DB_NAME"))

    cursor = db.cursor()
    electionId = request.args.get('election_id')
    cursor.execute(
        "SELECT electoral_key, name, middle_name, mlastname, flastname FROM candidate WHERE election_id = '{}'".format(electionId))
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
    cursor.execute(
        "SELECT * FROM candidate WHERE electoral_key = '{}'".format(electoral_key))
    candidate = cursor.fetchall()
    return jsonify(candidate)


@app.route('/login/', methods=['POST'])
def login():
    login_access = Access(connection, cursor)
    electoral_key = request.form.get('electoral_key')
    password = request.form.get('pass')
    response = make_response(
        json.dumps(login_access.login(str(electoral_key), str(password)))
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/signup/', methods=['POST'])
def signup():
    signup_access = Access(connection, cursor)
    electoral_key = request.form.get('electoral_key')
    password = request.form.get('pass')
    mail = request.form.get('email')
    response = make_response(
        str(signup_access.register(str(electoral_key), str(password), str(mail)))
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

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
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/fake/user', methods=['GET'])
def fake_user():
    faking = Fakerism(connection, cursor)
    response_user = str(faking.fake_user())
    response = make_response(response_user, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/fake/voter', methods=['GET'])
def fake_voter():
    faking = Fakerism(connection, cursor)
    response_user = str(faking.fake_voter())
    response = make_response(response_user, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


if __name__ == "__main__":
    app.run(port=os.getenv("PORT"), debug=True)
