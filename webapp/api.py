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
    return flask.render_template('maps.html')

@app.route('/politicalconflicts/<year>')
def get_all_countries(year):
    ''' Returns a list of all the countries and relevant severity
    information for the year indicated. Countries are output in
    alphabetical order'''
    query = '''SELECT country, three_letter, year, intind, intviol, intwar, civviol, civwar, ethviol, ethwar FROM severity WHERE year={0} ORDER by country'''.format(year)
    country_list = []
    for row in _fetch_all_rows_for_query(query):
        severity_sum = row[3] + row[4] + row[5] + row[6] + row[7] + row[8] + row[9]  
        country_info = {'country':row[0], 'three_letter':row[1], 'year':row[2], 'sum' : severity_sum}
        
        query_details = '''SELECT description
               FROM detail
               WHERE {1} BETWEEN beginning AND ending 
               AND UPPER(three_letter) LIKE UPPER('%{0}%')'''.format(row[1], year)
        descrip = ''
        counter = 0
        for line in _fetch_all_rows_for_query(query_details):
            if counter != 0:
                descrip = descrip + ', ' + line[0]
            else:
                descrip = line[0]
            counter=counter+1
        country_info['description'] =  descrip
       
        query_two_letter = '''SELECT two_letter FROM idtranslate WHERE UPPER(three_letter) LIKE UPPER('%{0}%')'''.format(row[1])
        for item in _fetch_all_rows_for_query(query_two_letter):
            two_letter_code = item[0]
        country_info[two_letter_code] = descrip + str(severity_sum) 

        country_list.append(country_info)

    return json.dumps(country_list)

@app.route('/politicalconflicts/detail/<country>')
def get_most_severe(country):
    ''' Returns a list of dictionaries, 
    each of which describes the total severity of conflict
     in a specific country with keys ‘country’, ’three_letter’, ‘year’, ‘sum’ '''
    query = '''SELECT year, intind, intviol, intwar, civviol, civwar, ethviol, ethwar
               FROM severity
               WHERE UPPER(country) LIKE UPPER('%{0}%')
               ORDER by year'''.format(country)
    highest_severity = 0
    highest_year = 0
    severity_sum = 0
    for row in _fetch_all_rows_for_query(query):
        severity_sum = row[1] + row[2] + row[3] + row[4] + row[5] + row[6] + row[7]  
        if (severity_sum >= highest_severity):
            highest_year = row[0]
            highest_severity = severity_sum
    print(--------------------------------------------highest_year)   
    return get_all_countries(highest_year)

    
@app.route('/politicalconflicts/<country>/<year>')
def get_country_details(country, year):
    ''' a list of dictionaries, each of which describes the total severity of 
    conflict in a specific country with keys ’three_letter’, ‘country’, ‘year’, ‘sum’
    '''
    query_severity = '''SELECT three_letter, country, year, intind, intviol, intwar, civviol, civwar, ethviol, ethwar
               FROM severity
               WHERE year={1} 
               AND UPPER(country) LIKE UPPER('%{0}%')'''.format(country, year)
    severity_list = {}
    for row in _fetch_all_rows_for_query(query_severity):
        severity_sum = row[3] + row[4] + row[5] + row[6] + row[7] + row[8] + row[9]  
        severity_list= {'three_letter':row[0], 'country':row[1], 'year':row[2], 'intind':row[3], 'intviol':row[4],
        'intwar':row[5], 'civviol':row[6], 'civwar':row[7], 'ethviol':row[8], 'ethwar':row[9]}

    query_details = '''SELECT description
               FROM detail
               WHERE {1} BETWEEN beginning AND ending 
               AND UPPER(country) LIKE UPPER('%{0}%')'''.format(country, year)
    descrip = ''
    counter = 0
    for row in _fetch_all_rows_for_query(query_details):
        if counter != 0:
            descrip = descrip + ', ' + row[0]
        else:
            descrip = row[0]
        counter=counter+1

    country_details= {'description': descrip}
    description = [severity_list, country_details]
    return json.dumps(description)

@app.route('/politicalconflicts/twoletter/<year>')
def get_all_countries_two_letter(year):
    '''returns severity sum and two letter code'''
    query = '''SELECT country, three_letter, year, intind, intviol, intwar,  civviol, civwar, ethviol, ethwar FROM severity WHERE year={0} ORDER by country'''.format(year)
    country_list={}
    for row in _fetch_all_rows_for_query(query):
        severity_sum = row[3] + row[4] + row[5] + row[6] + row[7] + row[8] + row[9]
        country_code = row[1]
        query_two_letter = '''SELECT two_letter FROM idtranslate WHERE UPPER(three_letter) LIKE UPPER('%{0}%')'''.format(country_code)
        for item in _fetch_all_rows_for_query(query_two_letter):
            two_letter_code = item[0]
            country_list[two_letter_code] = severity_sum
    return json.dumps(country_list)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host='thacker.mathcs.carleton.edu', port=5147, debug=True)


