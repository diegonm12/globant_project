import json
import mysql.connector
from flask import *
import os
 
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

connection = mysql.connector.connect(
    user='root', password='root', host='mysql', port="3306", database='db')

@app.route('/', methods=['GET'])
def index():
    return "Service up"

@app.route('/load', methods=['POST'])
def load():
    #data_to_load would be a S3 key in a bucket
    if ('table' in request.args.keys() and 'file' in request.args.keys()):
        table = request.args['table']
        location =  'data_to_load/' + request.args['file'] + '.csv'
        create_table_statement = 'create table ' + table + 

        return table + ' ' + location
    else:
        return "Arguments 'table' and 'location' are required"


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=7007)