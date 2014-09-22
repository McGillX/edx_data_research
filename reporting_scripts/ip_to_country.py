'''
This module retrieve IP addresses for each student and maps their IP to a country
This is to determine the diversity of students who took a given course
The geoip module and GeoIP.dat file was used to map the IP address to a country

Each user may have multiple ips, so this module retrieves all the countries mapped to those ips
Disclaimer: The accuracy of the IP to Country cannot be determined as it is difficult to determine
if the IP is an actual IP or a proxy IP

At the end of the analysis, the results are used to create a Pie Chart to visualize the distribution

'''
import geoip
import csv
import matplotlib.pyplot as pyplot
from collections import Counter, defaultdict

from base_edx import EdXConnection
from generate_csv_report import CSV

# Change name of collection as required
connection = EdXConnection('tracking_atoc185x' )
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

output = CSV(ip_to_country, ['Username', 'IP Address', 'Country Code', 'Country'], output_file='ip_to_country.csv')
output.generate_csv()

# Following lines of code are used to create a pie chart using matplotlib
pie_chart_counter =  Counter([country[-1] for country in ip_to_country])
pie_chart_counter_filter = defaultdict(float)
for count in pie_chart_counter:
    count_per = float(pie_chart_counter[count]) * 100.0 / len(ip_to_country)
    if count_per < 1.0:
        pie_chart_counter_filter['Other'] += pie_chart_counter[count]
    else:
        pie_chart_counter_filter[count] = count_per
pie_chart_counter_filter['Other'] = float(pie_chart_counter_filter['Other']) * 100.0 / len(ip_to_country)
pie_chart_labels = [key + " %0.2f" % value for key,value in pie_chart_counter_filter.items()]
pyplot.axis('equal')
#pyplot.pie(pie_chart_counter.values(), labels=pie_chart_labels)
patches, text = pyplot.pie(pie_chart_counter_filter.values())
lgd = pyplot.legend(patches, pie_chart_labels, loc='center left', bbox_to_anchor=(-0.1, 1.), fontsize=8)
pyplot.title("Pie Chart of Location of Students for ATOC 185x")
pyplot.savefig('student_location_atoc185x.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
