import json
import mysql.connector
from flask import *
import yaml
import csv
 
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

connection = mysql.connector.connect(
    user='root', password='root', host='mysql', port="3306", database='db')

def read_yaml(input, filename):
    with open(f'{filename}.yml','r') as f:
        output = yaml.safe_load(f)
    return output[input]

def read_data_csv(filename):
    values = ""
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            values = values + str(row).replace("[","(").replace("]",")").replace('"',"/'") + ","
    return values[:-1]

@app.route('/', methods=['GET'])
def index():
    return "Service up"

@app.route('/load', methods=['POST'])
def load():
    #data_to_load would be a S3 key in a bucket
    if ('table' in request.args.keys() and 'file' in request.args.keys()):
        table = request.args['table']
        file = request.args['file']
        location =  'data/' + file + '.csv'

        mycursor = connection.cursor()

        # creating the table if not exist
        table_layout = read_yaml(file, "data_layout/layout")
        create_table_statement = 'create table if not exists ' + table + ' ' + table_layout

        mycursor.execute(create_table_statement)

        # inserting the data into db

        # read data
        insert_values = read_data_csv(location)

        table_insert_fields = read_yaml(file + "_insert", "data_layout/layout")

        insert_table_statement = 'insert into db.' + table + ' ' + table_insert_fields + ' values ' + insert_values + ';'

        #mycursor.execute(str(insert_table_statement))
        #connection.commit() 




        
        return insert_table_statement
    else:
        return "Arguments 'table' and 'location' are required"


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=7007)