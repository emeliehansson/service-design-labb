from flask import Flask, request
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

    return ' navigate to en annan sida'

@app.route('/seeds', methods=['GET'])
def seeds():
    # Returns a list of our seeds
    # return cursor.execute('SELECT * FROM seeds').fetchall()
    # if request.method == 'GET':
    #     response = cursor.execute('SELECT * FROM seeds')
    #     unpacked = [{k: seed[k] for k in seed.keys()} for seed in response.fetchall()]
    #     return '{"Seeds":' + str(unpacked).replace("'", '"') + '}'
    return 'lista med seeds'


# Route and function for listing specific plants by their id.
@app.route('/seeds/<id>', methods=['GET', 'DELETE'])
def seed_detail(id):
    if request.method == 'GET':
        # Get data from database
        plant_id = cursor.execute('SELECT p_id FROM seeds WHERE id =' + str(id)).fetchall()[0][0]

        # Get data from API 
        response = requests.request("GET", url1 + str(plant_id) + api_key)

        print(response)
        return str(response.text)
    elif request.method == 'DELETE':
        response = cursor.execute('DELETE FROM seeds WHERE id=' + str(id))
        con.commit()
        if (response.rowcount > 0):
            return 'Deleted', 200
        else:
            return 'Could not delete', 404


# @app.route('/docs')
# def home():


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
