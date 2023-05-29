import sqlite3
from flask import Flask, jsonify, request, abort, make_response
import jwt_utils
from flask_cors import CORS
import os
import json
from operator import itemgetter

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.debug = True

CORS(app)

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    if (payload["password"] == 'flask2023'):
        return {'token': jwt_utils.build_token()}
    else:
        return 'Unauthorized', 401

class Question():
	def init(self, title: str, text, image, position, possibleAnswers):
		self.title = title
		self.text = text
		self.image = image
		self.position = position
		self.possibleAnswers = possibleAnswers

def get_db_connection():
    connection = sqlite3.connect(currentdirectory + "\quiz.db")
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/rebuild-db', methods=['POST'])
def build_db():
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	table_names = cursor.fetchall()
	for table_name in table_names:
		if table_name[0] != 'sqlite_sequence':
			cursor.execute("DROP TABLE {};".format(table_name[0]))

	cursor.execute(
		'CREATE TABLE "questions" ( "id" INTEGER,"title" TEXT,"text" TEXT,"image" TEXT,"position" INTEGER,"possibleAnswers" TEXT,PRIMARY KEY("id" AUTOINCREMENT))')
	cursor.execute(
	    'CREATE TABLE "participations" ( "id" INTEGER, "playerName" TEXT, "answers" TEXT, "score" INTEGER, PRIMARY KEY("id" AUTOINCREMENT) )')

	conn.commit()

	conn.close()
	response = make_response("Ok")
	response.status_code = 200
	return response


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	conn = get_db_connection()
	size = conn.execute("SELECT count(*) FROM questions").fetchone()[0]
	participations = conn.execute(
	    "SELECT playerName, score FROM participations").fetchall()
	scores = []
	for row in participations:
		scores.append({'playerName': row[0], 'score': row[1]})
	conn.close()
	sorted_scores = sorted(scores, key=itemgetter('score'), reverse=True)
	return {"size": size, "scores": sorted_scores}


@app.route('/get-questions', methods=['GET'])
def GetQuestion():
	c = get_db_connection()
	rows = c.execute("SELECT * FROM questions").fetchall()
	data = []
	for row in rows:
		data.append({'id': row[0], 'title': row[1], 'text': row[2], 'image': row[3],
		            'position': row[4], 'possibleAnswers': json.loads(row[5])})
	c.close()
	return jsonify(data)

@app.route('/questions', methods=['GET'])
def getQuestionPosition():
	position = request.args.get("position")
	conn = get_db_connection()
	row = conn.execute("SELECT * FROM questions WHERE position = ?",
                        (position,)).fetchone()
	conn.close()
	if row is None:
		message = "Request respond Not Found"
		return make_response(message, 404)
	data = []
	data.append({'id': row[0], 'title': row[1], 'text': row[2], 'image': row[3],
	            'position': row[4], 'possibleAnswers': json.loads(row[5])})
	return jsonify(data[0])


@app.route('/questions/<id>', methods=['GET'])
def show_question(id):
	# retrieve the question with the specified ID from the database
	conn = get_db_connection()
	row = conn.execute("SELECT * FROM questions WHERE id = ?",(id,)).fetchone()
	conn.close()
	if row is None:
		message = "Request respond Not Found"
		return make_response(message, 404)
	data = []
	data.append({'id': row[0], 'title': row[1], 'text': row[2], 'image': row[3],
	            'position': row[4], 'possibleAnswers': json.loads(row[5])})
	return jsonify(data[0])

@app.route('/questions', methods=['POST'])
def AddQuestion():
	# Récupérer le token envoyé en paramètre
	auth_header = request.headers.get('Authorization')

	if auth_header is None:
		return 'Unauthorized', 401
	auth_type, auth_token = auth_header.split()

	if auth_type != 'Bearer':
		return 'Unauthorized', 401

	try:
		jwt_utils.decode_token(auth_token)
	except jwt_utils.TokenError:
		return 'Unauthorized', 401

	title = request.json['title']
	text = request.json['text']
	image = request.json['image']
	position = request.json['position']
	possibleAnswers = json.dumps(request.json['possibleAnswers'])
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("INSERT INTO questions (title, text, image, position, possibleAnswers) VALUES (?,?,?,?,?)",
	               (title, text, image, position, possibleAnswers))
	id = cursor.lastrowid
	conn.commit()

	conn.close()
	return {"id": id}, 200

@app.route('/questions/<id>', methods=['PUT'])
def UpdateQuestion(id):
	# Récupérer le token envoyé en paramètre
	auth_header = request.headers.get('Authorization')

	if auth_header is None:
		return 'Unauthorized', 401
	auth_type, auth_token = auth_header.split()

	if auth_type != 'Bearer':
		return 'Unauthorized', 401

	try:
		jwt_utils.decode_token(auth_token)
	except jwt_utils.TokenError:
		return 'Unauthorized', 401

	conn = get_db_connection()
	row = conn.execute("SELECT * FROM questions WHERE id = ?",(id,)).fetchone()
	if row is None:
		message = "Request respond Not Found"
		return make_response(message, 404)

	title = request.json['title']
	text = request.json['text']
	image = request.json['image']
	position = request.json['position']
	possibleAnswers = json.dumps(request.json['possibleAnswers'])
	
	cursor = conn.cursor()
	cursor.execute("UPDATE questions SET title=?, text=?, image=?, position=?, possibleAnswers=? WHERE id = ?",
	               (title, text, image, position, possibleAnswers, id))
	response = make_response("Request respond ok")
	response.status_code = 204
	conn.commit()
	conn.close()
	return response

@app.route('/questions/<id>', methods=['DELETE'])
def DeleteQuestion(id):
	# Récupérer le token envoyé en paramètre
	auth_header = request.headers.get('Authorization')

	if auth_header is None:
		return 'Unauthorized', 401
	auth_type, auth_token = auth_header.split()

	if auth_type != 'Bearer':
		return 'Unauthorized', 401

	try:
		jwt_utils.decode_token(auth_token)
	except jwt_utils.TokenError:
		return 'Unauthorized', 401

	conn = get_db_connection()
	row = conn.execute("SELECT * FROM questions WHERE id = ?",(id,)).fetchone()
	if row is None:
		message = "Request respond Not Found"
		return make_response(message, 404)
	cursor = conn.cursor()
	cursor.execute("DELETE FROM questions WHERE id = ?", (id,))
	
	response = make_response("Request respond ok")
	response.status_code = 204
	
	conn.commit()
	conn.close()
	
	return response

@app.route('/participations', methods=['POST'])
def AddParticipation():
	playerName = request.json['playerName']
	playerAnswers = request.json['answers']
	if len(playerAnswers) < 10 or len(playerAnswers) > 10:
		abort(400)
	score = 0
	conn = get_db_connection()
	questionsRows = conn.execute(
	    "SELECT possibleAnswers FROM questions").fetchall()
	answers = []
	for row in questionsRows:
		answers.append({'answer': json.loads(row[0])})
	correctAnswers = []
	for answer in answers:
		for i, a in enumerate(answer['answer']):
			if a['isCorrect']:
				correctAnswers.append(i+1)
				break
	# Iterate over the elements in array1
	for i in range(len(playerAnswers)):
        # If the elements at index i in the two arrays are equal, increase the score
		if playerAnswers[i] == correctAnswers[i]:
			score += 1
	conn.execute("INSERT INTO participations (playerName, answers, score) VALUES (?,?,?)",
	             (playerName, json.dumps(playerAnswers), score))
	conn.commit()
	conn.close()

	return {'playerName': playerName, 'score': score}

@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
	# Récupérer le token envoyé en paramètre
	auth_header = request.headers.get('Authorization')

	if auth_header is None:
		return 'Unauthorized', 401
	
	auth_type, auth_token = auth_header.split()
	if auth_type != 'Bearer':
		return 'Unauthorized', 401

	try:
		jwt_utils.decode_token(auth_token)
	except jwt_utils.TokenError:
		return 'Unauthorized', 401

    # Connect to the database
	c = get_db_connection()

    # Delete all participations from the database
	c.execute('DELETE FROM participations')
	c.commit()

    # Close the connection to the database
	c.close()

    # Return a response with status code 204
	return '', 204

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions():
	# Récupérer le token envoyé en paramètre
	auth_header = request.headers.get('Authorization')

	if auth_header is None:
		return 'Unauthorized', 401
	
	auth_type, auth_token = auth_header.split()
	if auth_type != 'Bearer':
		return 'Unauthorized', 401

	try:
		jwt_utils.decode_token(auth_token)
	except jwt_utils.TokenError:
		return 'Unauthorized', 401
    
	# Connect to the database
	c = get_db_connection()

    # Delete all rows from the questions table
	c.execute('DELETE FROM questions')
	c.commit()

    # Close the connection to the database
	c.close()

    # Return a response with status code 204
	return '', 204

if __name__ == "__main__":
    app.run()