#!/usr/bin/env python3
'''
    api.py
    Josh Pitkofsky Allie Warren, 30 April 2016
The api for the political violence visualizer.
'''
import sys
import flask
import json
import config
import psycopg2

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

def _fetch_all_rows_for_query(query):
    '''
    Returns a list of rows obtained from the countries database
    by the specified SQL query. If the query fails for any reason,
    an empty list is returned.
    '''
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print('Connection error:', e, file=sys.stderr)
        return []

    rows = []
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall() # This can be trouble if your query results are really big.
    except Exception as e:
        print('Error querying database:', e, file=sys.stderr)

    connection.close()
    return rows

@app.route('/') 
def get_main_page():
    ''' This is the only route intended for human users '''
    return flask.render_template('index.html')

@app.route('/politicalconflicts/<year>')
def get_all_countries(year):
    ''' Returns a list of all the countries and relevant severity
    information for the year indicated. Countries are output in
    alphabetical order'''
    query = '''SELECT country, three_letter, year, intind, intviol, intwar, civviol, civwar, ethviol, ethwar
    FROM severity
    WHERE year={1} 
    ORDER by country'''.format(country)
    country_list = []
    for rows in _fetch_all_rows_for_query(query):
        severity_sum = row[3] + row[4] + row[5] + row[6] + row[7] + row[8] + row[9]  
        country= {'country':row[0], 'three_letter':row[1], 'year':row[2], 'sum' : severity_sum}
        country_list.append(country)

    return json.dumps(country_list)

@app.route('/politicalconflicts/<country>')
def get_most_severe(country):
    ''' Returns a list of dictionaries, 
    each of which describes the total severity of conflict
     in a specific country with keys ‘country’, ’three_letter’, ‘year’, ‘sum’ '''
    query = '''SELECT year, intind, intviol, intwar, civviol, civwar, ethviol, ethwar
               FROM severity
               WHERE UPPER(country) LIKE UPPER('%{1}%')
               ORDER by year'''.format(year)
    highest_severity = 0
    highest_year = 0
    for rows in _fetch_all_rows_for_query(query):
        severity_sum = row[3] + row[4] + row[5] + row[6] + row[7] + row[8] + row[9]  
        if (severity_sum >= highest_severity):
            highest_year = row[2]
        
    return get_all_countries(highest_year)

    
@app.route('/politicalconflicts/<country>/<year>')
def get_country_details(country, year):
    ''' a list of dictionaries, each of which describes the total severity of 
    conflict in a specific country with keys ’three_letter’, ‘country’, ‘year’, ‘sum’
    '''
    query_severity = '''SELECT three_letter, country, year, intind, intviol, intwar, civviol, civwar, ethviol, ethwar
               FROM severity
               WHERE year={2} 
               AND UPPER(country) LIKE UPPER('%{1}%')'''
    severity_list = {}
    for rows in _fetch_all_rows_for_query(query_severity):
        severity_sum = row[3] + row[4] + row[5] + row[6] + row[7] + row[8] + row[9]  
        severity_list= {'three_letter':row[0], 'country':row[1], 'year':row[2], 'intind':row[3], 'intviol':row[4],
        'intwar':row[5], 'civviol':row[6], 'civwar':row[7], 'ethviol':row[8], 'ethwar':row[9]}

    query_details = '''SELECT description
               FROM detail
               WHERE beginning <= {2} AND {2} <= ending 
               AND UPPER(country) LIKE UPPER('%{1}%')'''
    country_details = {}
    for rows in _fetch_all_rows_for_query(query_details): 
        country_details = {'description':row[0]}
    
    description = [severity_list, country_details]
    return json.dumps(description)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)


