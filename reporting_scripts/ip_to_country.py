'''
This module retrieve IP addresses for each student and maps their IP to a country
This is to determine the diversity of students who took a given course
The geoip module and GeoIP.dat file was used to map the IP address to a country

Each user may have multiple ips, so this module retrieves all the countries mapped to those ips
Disclaimer: The accuracy of the IP to Country cannot be determined as it is difficult to determine
if the IP is an actual IP or a proxy IP

At the end of the analysis, the results are used to create a Pie Chart to visualize the distribution

Usage:
python ip_to_country.py <db_name>

'''
import geoip
import csv
from collections import Counter, defaultdict
import sys

from base_edx import EdXConnection
from generate_csv_report import CSV

db_name = sys.argv[1]

# Change name of collection as required
connection = EdXConnection(db_name, 'tracking' )
collection = connection.get_access_to_collection()

# The csv file country_code_to_country.csv was retrieved from http://dev.maxmind.com/geoip/legacy/geolite/
# This was used to get a mapping of a country code to a country
with open('country_code_to_country.csv') as f:
    reader = csv.reader(f)
    country_code_to_country = dict(reader)

cursor = collection['tracking'].find()
result = {}
for index, item in enumerate(cursor):
    if item['username'] not in result:
	    result[item['username']] = {item['ip']}
    else:
	    result[item['username']].add(item['ip'])
ip_to_country = []
country_set = set() #defaultdict(set)
for key in result:
    for value in result[key]:
        try:
            country_code = geoip.country(value)
            country = country_code_to_country[country_code]
            if (key, country) not in country_set:
                country_set.add((key,country))
                ip_to_country.append([key, value, country_code, country])
        except:
            # IMPORTANT
            # The following code for an exception are hardcoded for those IPs which do have a mapping to a 
            # country code but they were not available in GeoIP.dat (most probably because it was not updated)
            # People using this script can either report this code (under except) and or additional conditions
            # IP addresses which cannot be mapped to a country code stored in GeoIP.dat
            if value == '41.79.120.29':
                country = country_code_to_country['SS']
                if (key, country) not in country_set:
                    country_set.add((key, country))
                    ip_to_country.append([key, value, 'SS', country_code_to_country['SS']])

output = CSV(ip_to_country, ['Username', 'IP Address', 'Country Code', 'Country'], output_file=db_name+'_ip_to_country.csv')
output.generate_csv()
