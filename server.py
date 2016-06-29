from flask import Flask, session, redirect, render_template, request, jsonify
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = "sdghejrehwgafc"
mysql = MySQLConnector(app, "ajax_notes")

@app.route('/')
def index():
	query = "SELECT * FROM notes"
	notes = mysql.query_db(query)
	return render_template('index.html', notes=notes)

@app.route('/desc/<id>', methods=['POST'])
def description(id):
	query = "UPDATE notes SET description = :description, updated_at = NOW() WHERE id = :id LIMIT 1"
	data = {
		'description': request.form['description'],
		'id': id
	}
	mysql.query_db(query, data)
	return redirect('/update')

@app.route('/update')
def update():
	query = "SELECT * FROM notes"
	notes = mysql.query_db(query)
	print "/n/n/n/n/n/n" , notes
	return render_template('partial.html', notes=notes)


@app.route('/new', methods=['POST'])
def new():
	data = {
		'title': request.form['title']

	}
	query = "INSERT INTO notes (title, created_at, updated_at) VALUES (:title, NOW(), NOW())"

	mysql.query_db(query, data)
	return redirect('/')

@app.route('/delete/<id>')
def delete(id):
	query = "DELETE FROM notes WHERE id = :id LIMIT 1"
	data = {
		'id': id
	}
	mysql.query_db(query, data)
	return redirect('/update')




app.run(debug=True)
