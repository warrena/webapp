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
    ''' This is the only route intended for human users
    It features an interactive world map that displays political conflicts
    worldwide that occurred between 1946 and 2012'''
    return flask.render_template('maps.html')

@app.route('/politicalconflicts/<year>/<two_letter_code>')
def get_all_countries(year, two_letter_code):
    ''' Returns the severity information (severity sum and description of the conflict)
    for the specified country in the specified year. Countries are identified using the two letter country code.
    This is being used by the webpage to get the information that display below the map.'''
    query_two_letter = '''SELECT three_letter FROM idtranslate WHERE UPPER(two_letter) LIKE UPPER('%{0}%')'''.format(two_letter_code)
    for item in _fetch_all_rows_for_query(query_two_letter):
        three_letter_code = item[0]
    query = '''SELECT country, three_letter, year, intind, intviol, intwar, civviol, civwar, ethviol, ethwar FROM severity WHERE year={0} AND UPPER(three_letter) LIKE UPPER('%{1}%')'''.format(year, three_letter_code)
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

@app.route('/politicalconflicts/highestYear/<country>')
def get_most_severe_year(country):
    '''Finds the year that had the highest severity for the specified country,
    then uses that year to get list of dictionaries that contain 
    each country in the map and the severity level for that country in the year found 
    (using the get_all_countries_two_letter api call)
    This is used by the webpage to update the map when a country is entered'''
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
    return json.dumps(highest_year)

@app.route('/politicalconflicts/detail/<country>') 
def get_most_severe(country):
    '''Finds the year that had the highest severity for the specified country and returns that year'''   
    highest_year = get_most_severe_year(country)
    return get_all_countries_two_letter(highest_year)

    
@app.route('/politicalconflicts/<country>/<year>')
def get_country_details(country, year):
    ''' a list of dictionaries, each of which describes the total severity of 
    conflict in a specific country with keys ’three_letter’, ‘country’, ‘year’, ‘sum’
    This is not currently being used by the website.
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
    '''Returns a list of  dictionaries containing a key which is the two letter code
    for the country and the value which is the total severity sum for that country. This
    information is gathered for every country in the year specified.
    This api call is used by the main year search feature of the map'''
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


