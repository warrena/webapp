'''
   api_tests.py
   Josh Pitkofsky and Allie Warren, 24 April 2016
   Adapted from Jeff Ondich's code
'''

import apichecker
import unittest

class ApiTester(unittest.TestCase):
    def setUp(self):

        self.Api_checker = apichecker.ApiTester()

    def tearDown(self):

        self.Api_checker = null

    def testCountrySeverityData(self):
        self.assertEqual(self.Api_checker.get_severity('CHN', 1990),{'intind':0,'intviol':0,'intwar':0,'civviol':0,'civwar':1,'ethviol':2,'ethwar':0})

    def testCountrySeverityDataDoesNotExist(self):
        self.assertEqual(self.Api_checker.get_severity('NFK', 1950),{''})

    def testCountryDescriptionDataDoesNotExist(self):
        self.assertEqual(self.Api_checker.get_description('NFK', 1950),[''])

    def testMultipleDescriptions(self):
        self.assertEqual(self.Api_checker.get_description('CHN', 1950), [ {'description': 'international violence (formosa straits)', 'tibet invasion', 'repression of landlords', 'korean civil war'}])

    def testGetThree(self):
        self.assertEqual(self.Api_checker.get_three('AF'), "AFG")

    def testGetTwo(self):
        self.assertEqual(self.Api_checker.get_two('AFG'), "AF")

    def testWorstYear(self):
        self.assertEqual(self.Api_checker.get_worst('CHN'), [ {'year': 1950} ])

    def testManyWorstYears(self):
        self.assertEqual(self.Api_checker.get_worst('IRQ'), [ {'year': 1980} ])

    def testYearDoesNotExist(self):
        self.assertEqual(self.Api_checker.get_description('GUA', 1970), [''])

    def testNoEndSameYear(self):
        self.assertEqual(self.Api_checker.get_description('IND', 1999), [ {'description': 'international violence (kargil clashes)'} ] )

    def testNoEndOngoing(self):
        self.assertEqual(self.Api_checker.get_description('TUR', 2005), [ {'description': 'kurds in the southeast'} ] )

    def testYearGeneric(self):
        self.assertEqual(self.Api_checker.get_year(1946), ['CHN','GRC', 'FRN', 'IRN', 'BOL', 'AFG', 'ALB', 'ALG', 'ARG', 'AUL', 'AUS', 'BEL', 'BRA', 'BUL', 'CAN', 'CHL', 'COL', 'COS', 'CUB', 'CZE', 'DEN', 'DOM', 'ECU', 'SAL', 'ETH', 'FIN', 'GUA', 'HAI', 'HON', 'HUN', 'IRQ', 'IRE', 'ITA', 'JPN', 'JOR', 'LEB', 'LBR', 'LUX', 'MEX', 'MON', 'NEP', 'NTH', 'NEW', 'NIC', 'NOR', 'PAN', 'PAR', 'PER', 'PHI', 'POL', 'POR', 'RUM', 'SAU', 'SAF', 'SPN', 'SWD', 'SWZ', 'SYR', 'THI', 'TUR', 'UKG', 'USA', 'URU', 'USR', 'VEN', 'YAR', 'YUG', 'IND', 'INS', 'PAK', 'VIE'])

if __name__ == '__main__':
    unittest.main()
