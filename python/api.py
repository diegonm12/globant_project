import json
import mysql.connector
from flask import Flask
app = Flask(__name__)

connection = mysql.connector.connect(
    user='root', password='root', host='mysql', port="3306", database='db')

@app.route('/', methods=['GET'])
def index():
    return "Service up"
if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=7007)