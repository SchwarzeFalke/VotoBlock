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

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def index():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    response = make_response(str('Welcome to VotoBlock!'))
    response.headers.add('Access-Control-Allow-Origin', '*')
    connection.close()
    return response


@app.route('/verify/elections/', methods=['GET'])
def verifyElectionPeriod():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    db = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                 host=os.getenv("DB_HOST"),
                                 database=os.getenv("DB_NAME"))

    cursor = db.cursor()
    cursor.execute("SELECT _id, descript FROM election")
    elections = cursor.fetchall()
    connection.close()
    return jsonify(elections)


@app.route('/election/', methods=['GET'])
def getElectionResults():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
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
    connection.close()
    return jsonify(elections)


@app.route('/verify/candidates/', methods=['GET'])
def verifyAvailableCandidates():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    db = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                 host=os.getenv("DB_HOST"),
                                 database=os.getenv("DB_NAME"))

    cursor = db.cursor()
    electionId = request.args.get('election_id')
    cursor.execute(
        "SELECT electoral_key, name, middle_name, mlastname, flastname FROM candidate WHERE election_id = '{}'".format(electionId))
    results = cursor.fetchall()
    candidates = []
    for row in results:
        tempData = {
            "electoral_key": row[0],
            "full_name": row[1] + ' ' + row[2] + ' ' + row[3] + ' ' + row[4]
        }
        candidates.append(tempData)
    connection.close()
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
    connection.close()
    return jsonify(candidate)


@app.route('/login/', methods=['POST'])
def login():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    login_access = Access(connection, cursor)
    electoral_key = request.form.get('electoral_key')
    password = request.form.get('pass')
    response = make_response(
        json.dumps(login_access.login(str(electoral_key), str(password)))
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    connection.close()
    return response


@app.route('/signup/', methods=['POST'])
def signup():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    signup_access = Access(connection, cursor)
    electoral_key = request.form.get('electoral_key')
    password = request.form.get('pass')
    mail = request.form.get('email')
    response = make_response(
        str(signup_access.register(str(electoral_key), str(password), str(mail)))
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    connection.close()
    return response

# Section: Vote routes
@app.route('/vote', methods=['GET'])
def getVote():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    vote = Vote(connection, cursor)
    voteKey = request.form.get('vote')
    response = make_response(
        str(vote.retrieveVote(voteKey))[2:-1]
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    connection.close()
    return response


@app.route('/vote', methods=['POST'])
def postVote():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
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
    connection.close()
    return response


@app.route('/fake/user', methods=['GET'])
def fake_user():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    faking = Fakerism(connection, cursor)
    response_user = str(faking.fake_user())
    response = make_response(response_user, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    connection.close()
    return response


@app.route('/fake/voter', methods=['GET'])
def fake_voter():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    faking = Fakerism(connection, cursor)
    response_voter = str(faking.fake_voter())
    response = make_response(response_voter, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    connection.close()
    return response


@app.route('/fake/candidate', methods=['GET'])
def fake_candidate():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    faking = Fakerism(connection, cursor)
    response_candidate = str(faking.fake_candidate())
    response = make_response(response_candidate, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    connection.close()
    return response


@app.route('/img/party/', methods=['GET'])
def verifyAvailableCandidates():
    connection = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                         host=os.getenv("DB_HOST"),
                                         database=os.getenv("DB_NAME"))
    cursor = connection.cursor()
    db = mysql.connector.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"),
                                 host=os.getenv("DB_HOST"),
                                 database=os.getenv("DB_NAME"))

    cursor = db.cursor()
    electoral_key = request.args.get('electoral_key')
    cursor.execute(
        "SELECT party_id FROM candidate WHERE electoral_key = '{}'".format(electoral_key))
    results = cursor.fetchall()
    party_id = results[0][0]
    cursor.execute(
        "SELECT logo FROM party WHERE _id = '{}'".format(party_id))
    results = cursor.fetchall()
    blob = results[0][0]
    connection.close()
    return(blob)


if __name__ == "__main__":
    app.run(port=os.getenv("PORT"), debug=True)
