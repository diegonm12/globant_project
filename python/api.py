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
    values = []
    wrong_values = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if '' in row:
                wrong_values.append(tuple([filename, str(row)]))
            else:
                values.append(tuple(row))
    return [values,wrong_values]

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
        create_table_statement_wrong_data = 'create table if not exists error_logs (table_affected VARCHAR(50), query VARCHAR(200))'

        mycursor.execute(create_table_statement)
        mycursor.execute(create_table_statement_wrong_data)

        # inserting the data into db

        # read data
        insert_values = read_data_csv(location)

        table_insert_fields = read_yaml(file + "_insert", "data_layout/layout")

        insert_table_statement = 'insert into db.' + table + ' ' + table_insert_fields
        insert_table_statement_wrong_data = 'insert into db.error_logs' + ' ' +  '(table_affected, query) values (%s, %s)'

        mycursor.executemany(insert_table_statement, insert_values[0])
        mycursor.executemany(insert_table_statement_wrong_data, insert_values[1])

        connection.commit()
        
        return "operation done"
    else:
        return "Arguments 'table' and 'location' are required"


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=7007)