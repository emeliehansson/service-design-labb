from flask import Flask, render_template
import sqlite3

# Create a Flask Instance
app = Flask(__name__)

# Connect to database
db = sqlite3
con = sqlite3.connect('plants.db')

# Initalize database
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/docs')
# def home():

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
