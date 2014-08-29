'''
This module maps the ip address of a student to a corresponding country using the 
geoip module found online

Each user may have multiple ips, so this module retrieves all the countries mapped to those ips
Disclaimer: The accuracy of the IP to Country cannot be determined as it is difficult to determine
if the IP is an actual IP or a proxy IP

geoip uses GeoIP.dat to map ip address to a country
'''

from pymongo import MongoClient
from pprint import pprint
import geoip
import csv

DATABASE_ADDRESS = "mongodb://localhost"
DATABASE_NAME = 'edx'
DATABASE_TRACKING_COLLECTION = 'tracking'

client = MongoClient(DATABASE_ADDRESS)
db = client[DATABASE_NAME]
tracking = db[DATABASE_TRACKING_COLLECTION]
cursor = tracking.find()
result = {}
for index, item in enumerate(cursor):
    if item['username'] not in result:
	result[item['username']] = {item['ip']}
    else:
	result[item['username']].add(item['ip'])
ip_to_country = {}
with open('ip_to_country.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Username', 'IP Address', 'Country'])
    for key in result:
        ip_to_country[key] = []
        for value in result[key]:
	       writer.writerow([key, value, geoip.country(value)])