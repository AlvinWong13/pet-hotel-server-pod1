from flask import Flask, request, jsonify, make_response
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    print('we made it to the server')
    return "<h1>Hello Pet World!</h1><p>I Am in python flask</p>"

@app.route('/owners', methods=['GET'])
def get_owners():
    # connection to postgresDB
    connection = psycopg2.connect(user="", host="127.0.0.1", port="5432", database="pethotel")
    # avoid getting arrays of arrays
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query_text = "SELECT owners.id, owners.name, COUNT(pets.name) AS count FROM owners JOIN pets ON owners.id = pets.owner_id GROUP BY owners.id, owners.name"
    # execute query
    cursor.execute(query_text)
    #Select rows from table using cursor.fetchall
    owners = cursor.fetchall()
    print(owners)
    #response 200
    return jsonify(owners)

@app.route('/owners', methods=['POST'])
def add_owner():
  print('in addOwners')
  request_data = request.get_json()
  name = request_data['name']
  # connection to postgresDB
  connection = psycopg2.connect(user="", host="127.0.0.1", port="5432", database="pethotel")
  # avoid getting arrays of arrays
  cursor = connection.cursor(cursor_factory=RealDictCursor)
  print(name)
  query_text = "INSERT INTO owners (name) VALUES ('%s');" 
  # execute query
  cursor.execute(query_text % (name,))
  # commit the query
  connection.commit()
  #response 201
  return '''OK'''

app.run()