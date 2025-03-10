from flask import Flask, request, jsonify
import sqlite3
import requests

# Create a Flask Instance
app = Flask(__name__)

# Connect to database
con = sqlite3.connect('plants.db', check_same_thread=False)
cursor = con.cursor()
con.row_factory = sqlite3.Row

# Förkortad url för details
url1 = "https://perenual.com/api/species/details/"

filename = 'apikey'

def get_file_contents(filename):
    """ Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)
    
api_key = get_file_contents(filename)

@app.route('/')
def home():
    return 'Welcome to this API'

# Route and function for listing all seeds from the database.
@app.route('/seeds', methods=['GET'])
def seeds():
    # Returns a list of our seeds
    if request.method == 'GET':
        response = cursor.execute('SELECT * FROM seeds')
        columns = [column[0] for column in cursor.description]
        unpacked = [dict(zip(columns, row)) for row in response.fetchall()]
        if (response.rowcount == 0): 
            return 'List is empty', 204
        return jsonify({"Seeds": unpacked}), 200
    else:
        return 'Could not implement your request', 400


# Route and function for listing specific plants by their id.
@app.route('/seeds/<id>', methods=['GET', 'DELETE'])
def seed_detail(id):
    if request.method == 'GET':
        # Get data from database
        plant_id_row = cursor.execute('SELECT p_id FROM seeds WHERE id =' + str(id)).fetchone()
        if plant_id_row == None:
            return 'ID does not exist', 404
        
        plant_id = plant_id_row[0]

        # Get data from API 
        response = requests.request("GET", url1 + str(plant_id) + api_key)
        return jsonify(response.json()), 200
    elif request.method == 'DELETE':
        response = cursor.execute('DELETE FROM seeds WHERE id=' + str(id))
        con.commit()
        if (response.rowcount > 0):
            return 'Deleted', 200
        else:
            return 'Could not delete', 404


@app.route('/api/docs')
def documentation():
    return open('docs/docs.yaml')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
