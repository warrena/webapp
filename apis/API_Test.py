
#!/usr/bin/env python3
'''
    api_test.py
    Josh Pitkofsky adapted from Jeff Ondich's code, 13 April 2016
    For CS 257 Software Design. 
'''

import sys
import argparse
import json
import urllib.request



def get_weather_city(city):
    '''
    Returns a list of weather information for the specified place. The weather is represented as
    dictionaries of the form
    
       {'description':..., 'detailed_description':...}

    For example, the results for get_city_details('newyork')
    would be:

       [{'description':'rain', 'detailed_description':'light rain'} ]
    '''
    base_url = "http://api.openweathermap.org/data/2.5/weather?q={0}&appid=159f4e6896f178b82eeec08d44b63299"
    url = base_url.format(city)

    try:
        data_from_server = urllib.request.urlopen(url).read()
        string_from_server = data_from_server.decode('utf-8')
        weather_info_list = json.loads(string_from_server)
    except Exception as e:
        # Problems with network access or JSON parsing.
        return []

    result_list = []
    try:
        description = weather_info_list["weather"][0]["main"]
        detailed_description = weather_info_list["weather"][0]["description"]
        if type(description) != type(''):
            raise Exception('city has no weather: "{0}"'.format(description))      
        if type(detailed_description) != type(''):
            raise Exception('city does not exist: "{0}"'.format(detailed_description))
        result_list.append({'description':description, 'detailed_description':detailed_description})
    except Exception as e:
        pass
    return result_list

def get_weather_zip(zipCode):
    '''
    Returns a list of weather information for the specified Zip. The weather is represented as
    dictionaries of the form
    
       {'description':..., 'detailed_description':...}

    For example, the results for get_city_details('94070')
    would be:

       [{'description':'rain', 'detailed_description':'light rain'} ]
    '''
    base_url = "http://api.openweathermap.org/data/2.5/weather?zip={0},us&appid=159f4e6896f178b82eeec08d44b63299"
    url = base_url.format(zipCode)

    try:
        data_from_server = urllib.request.urlopen(url).read()
        string_from_server = data_from_server.decode('utf-8')
        weather_info_list = json.loads(string_from_server)
    except Exception as e:
        # Problems with network access or JSON parsing.
        return []

    result_list = []
    try:
        description = weather_info_list["weather"][0]["main"]
        detailed_description = weather_info_list["weather"][0]["description"]
        if type(description) != type(''):
            raise Exception('city has no weather: "{0}"'.format(description))      
        if type(detailed_description) != type(''):
            raise Exception('city does not exist: "{0}"'.format(detailed_description))
        result_list.append({'description':description, 'detailed_description':detailed_description})
    except Exception as e:
        pass
    return result_list

def get_humidity_city(city):
    '''
    Returns humidity information for the specified city.
    
       {'humidity':..}

    For example, the results for get_humidity_city('newyork')
    would be:

       [{'humidity':89} ]
    '''
    base_url = "http://api.openweathermap.org/data/2.5/weather?q={0}&appid=159f4e6896f178b82eeec08d44b63299"
    url = base_url.format(city)

    try:
        data_from_server = urllib.request.urlopen(url).read()
        string_from_server = data_from_server.decode('utf-8')
        weather_info_list = json.loads(string_from_server)
    except Exception as e:
        # Problems with network access or JSON parsing.
        return []

    result_list = []
    try:
        humidity = weather_info_list["main"].get("humidity")
        humidity=str(humidity)
        if type(humidity) != type(''):
            raise Exception('city has no humidity: "{0}"'.format(humidity))      
        result_list.append({'humidity': humidity })
    except Exception as e:
        pass
    return result_list


def main(args):

    if args.action == 'weather':
        city_details = get_weather_city(args.place)

        for city_detail in city_details:
            description = city_detail['description']
            detailed_description = city_detail['detailed_description']
            print('Weather: {0} \nDetails: {1}'.format(description, detailed_description))

    elif args.action == 'zipcode':
        city_details = get_weather_zip(args.place)

        for city_detail in city_details:
            description = city_detail['description']
            detailed_description = city_detail['detailed_description']
            print('Weather: {0} \nDetails: {1}'.format(description, detailed_description))

    elif args.action == 'humidity':
        city_humidity = get_humidity_city(args.place)
        for city_detail in city_humidity:
            humidity = city_detail['humidity']
            print('humidity in {0} is: {1}%'.format(args.place, humidity))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get weather info from the Open Weather API')

    parser.add_argument('action',
                        metavar='action',
                        help='action to perform on the location ("weather" or "humidity"), if you want weather from a zipcode, use zipcode',
                        choices=['weather', 'humidity','zipcode'])

    parser.add_argument('place', help='the place you want to know about, if your action was zipcode, use a zipcode')

    args = parser.parse_args()
    main(args)