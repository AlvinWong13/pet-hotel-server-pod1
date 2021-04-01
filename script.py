from flask import Flask, request, jsonify, make_response
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    print('we made it to the server')
    return "<h1>Hello Pet World!</h1><p>I Am in python flask</p>"
    
# OWNERS ROUTES START

@app.route('/owners', methods=['GET'])
def get_owners():
    # connection to postgresDB
    connection = psycopg2.connect(user="", host="127.0.0.1", port="5432", database="pethotel")
    # avoid getting arrays of arrays
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query_text = "SELECT owners.id, owners.name, COUNT(pets.name) AS count FROM owners LEFT JOIN pets ON owners.id = pets.owner_id GROUP BY owners.id, owners.name;"
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
  count = cursor.rowcount
  print(count, 'owner inserted')
  result = {'status': 'CREATED'}
  #response 201
  return make_response(jsonify(result),201)

@app.route('/owners/<int:id>', methods=['DELETE'])
def delete_owner(id):
  print('in deleteOwner')
  # connection to postgresDB
  connection = psycopg2.connect(user="", host="127.0.0.1", port="5432", database="pethotel")
  # avoid getting arrays of arrays
  cursor = connection.cursor(cursor_factory=RealDictCursor)
  query_text = "DELETE FROM owners where id = '%s';"
  cursor.execute(query_text % (id,))
  connection.commit()
  count = cursor.rowcount
  result = {'status': 'deleted'}
  return make_response(jsonify(result), 201)

# OWNERS ROUTES END

# PETS ROUTES START

@app.route('/pets', methods=['GET'])
def get_pets():
    # connection to postgresDB
    connection = psycopg2.connect(user="", host="127.0.0.1", port="5432", database="pethotel")
    # avoid getting arrays of arrays
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    query_text = "SELECT pets.id, owners.name AS owner, pets.name, pets.breed, pets.color, pets.checkin FROM pets JOIN owners ON owners.id = pets.owner_id;"
    # execute query
    cursor.execute(query_text)
    #Select rows from table using cursor.fetchall
    pets = cursor.fetchall()
    print(pets)
    #response 200
    return jsonify(pets)

@app.route('/pets', methods=['POST'])
def add_pet():
  print('in add_pet')
  request_data = request.get_json()
  owner = request_data['owner']
  name = request_data['name']
  breed = request_data['breed']
  color = request_data['color']
  # connection to postgresDB
  connection = psycopg2.connect(user="", host="127.0.0.1", port="5432", database="pethotel")
  # avoid getting arrays of arrays
  cursor = connection.cursor(cursor_factory=RealDictCursor)
  query_text = "INSERT INTO pets (owner_id, name, breed, color) VALUES ('%s', '%s', '%s', '%s')" 
  # execute query
  cursor.execute(query_text % (owner, name, breed, color,))
  # commit the query
  connection.commit()
  count = cursor.rowcount
  print(count, 'owner inserted')
  result = {'status': 'CREATED'}
  #response 201
  return make_response(jsonify(result),201)

@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pets(id):
  print('in delete_pets')
  # connection to postgresDB
  connection = psycopg2.connect(user="", host="127.0.0.1", port="5432", database="pethotel")
  # avoid getting arrays of arrays
  cursor = connection.cursor(cursor_factory=RealDictCursor)
  query_text = "DELETE FROM pets where id = '%s';"
  cursor.execute(query_text % (id,))
  connection.commit()
  count = cursor.rowcount
  result = {'status': 'deleted'}
  return make_response(jsonify(result), 201)

@app.route('/pets/<int:id>', methods=['PUT'])
def pet_checkin(id):
  print('in checkin')
  # connection to postgresDB
  connection = psycopg2.connect(user="", host="127.0.0.1", port="5432", database="pethotel")
  # avoid getting arrays of arrays
  cursor = connection.cursor(cursor_factory=RealDictCursor)
  query_text = "UPDATE pets SET checkin = (CASE WHEN checkin is NULL THEN CURRENT_DATE ELSE NULL END) WHERE id = '%s';" 
  # execute query
  cursor.execute(query_text % (id,))
  # commit the query
  connection.commit()
  count = cursor.rowcount
  result = {'status': 'updated'}
  #response 201
  return make_response(jsonify(result),201)

# PETS ROUTES START

app.run()