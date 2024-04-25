from flask import Flask, request
import sqlite3
import requests
import json

# Create a Flask Instance
app = Flask(__name__)

# Connect to database

con = sqlite3.connect('plants.db', check_same_thread=False)
cursor = con.cursor()
# url till hela listan
# url = "https://perenual.com/api/species-list?key=sk-FfKw662a5376cb5285251"
# förkortad url för details
url1 = "https://perenual.com/api/species/details/"
# Hemlig API nyckel till perenual
api_key = '?key=sk-FfKw662a5376cb5285251'



@app.route('/')
def home():

    return ' navigate to en annan sida'

@app.route('/seeds')
def items():
    # return list of seeds
    # api listan = https://perenual.com/api/species-list?key=sk-FfKw662a5376cb5285251
    return cursor.execute('SELECT * FROM seeds').fetchall()

# Nu hämtar den id nr från adressen och gör om den till plant_id för att passa in i url adressen. Tyvärr hämtar den inte från DB, men det funkar
@app.route('/seeds/<ID>', methods=['GET'])
def seed(ID):
    if request.method == 'GET':
        # kod från Jimmy
        # github_user = cursor.execute('SELECT name FROM seeds WHERE ID =' + str(ID)).fetchall()[0][0]
        # user_details = requests.get(url1 + github_user)

        # Kod från api sidan
        payload = {}
        headers = {}
        plant_id = ID

        response = requests.request("GET", url1 + plant_id + api_key,  headers=headers, data=payload)

        print(response)
        return str(response.text)

# @app.route('/docs')
# def home():


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
