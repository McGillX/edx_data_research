import csv
import os

from collections import defaultdict, namedtuple

from edx_data_research.reporting.edx_base import EdX
from edx_data_research.reporting.lib import geoip

class Basic(EdX):

    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        self.basic_cmd = args.basic.replace('-', '_')

    def user_info(self):
        '''Retrieve info about students registered in given course'''
        self.collections = ['certificates_generatedcertificate',
                            'auth_userprofile','user_id_map',
                            'student_courseenrollment']
        cursor = self.collections['auth_userprofile'].find()
        result = []
        for item  in cursor:
            user_id = item['user_id']
            try:
                final_grade = (self.collections['certificates_generatedcertificate']
                               .find_one({'user_id' : user_id})['grade'])
                user_id_map = (self.collections['user_id_map']
                               .find_one({'id' : user_id}))
                username = user_id_map['username']
	        hash_id = user_id_map['hash_id']
                enrollment_date = (self.collections['student_courseenrollment']
                                   .find_one({'user_id' : user_id})['created'])
                row = self.anonymize_row([hash_id], [user_id, username],
                                         [item['name'], final_grade,
                                         item['gender'], item['year_of_birth'],
                                         item['level_of_education'],
                                         item['country'], item['city'],
                                         enrollment_date])
                result.append(row)
            except KeyError:
                print "Exception occurred for user_id {0}".format(user_id)
        headers = self.anonymize_headers(['Name', 'Final Grade', 'Gender',
                                          'Year of Birth', 'Level of Education',
                                          'Country', 'City', 'Enrollment Date'])
        report_name = self.report_name(self.db.name, self.basic_cmd)
        self.generate_csv(result, headers, report_name)

    def course_completers(self):
        '''
        Extract the student IDs from the collection
        certificates_generatedcertificate of the students who completed the
        course and achieved a certificate. The ids are then used to extract
        the usernames of the course completers
        '''
        self.collections = ['certificates_generatedcertificate', 'auth_user',
                            'user_id_map']
        cursor = (self.collections['certificates_generatedcertificate']
                  .find({'status' : 'downloadable'}))
        result = []
        for item in cursor:
            user_document = (self.collections['auth_user']
                             .find_one({"id" : item['user_id']}))
            user_id = user_document['id']
            hash_id = (self.collections['user_id_map']
                       .find_one({'id' : user_id})['hash_id'])
            row = self.anonymize_row([hash_id],
                                     [user_id, user_document['username']],
                                     [item['name'], item['grade']])
            result.append(row)
        headers = self.anonymize_headers(['Name', 'Grade'])
        report_name = self.report_name(self.db.name, self.basic_cmd)
        self.generate_csv(result, headers, report_name)

    def forum(self):
        '''Retrieve info from the forum collection for a given course'''
        self.collections = ['forum', 'user_id_map']
        cursor = self.collections['forum'].find()
        result = []
        for item in cursor:
            user_id = int(item['author_id'])
            hash_id = (self.collections['user_id_map']
                       .find_one({'id' : user_id})['hash_id'])
            row = self.anonymize_row([hash_id],
                                     [user_id, item['author_username']],
                                     [item['_type'], item.get('title', ''),
                                      item['body'], item['created_at']])
            result.append(row)
        headers = self.anonymize_headers(['Type', 'Title', 'Body',
                                          'Created At Date'])
        report_name = self.report_name(self.db.name, self.basic_cmd)
	self.generate_csv(result, headers, report_name)

    def ip_to_country(self):
        self.collections = ['tracking', 'user_id_map']
        data_directory = os.path.abspath(os.path.dirname(__file__) + "/data")
        with open(os.path.join(data_directory, 'country_code_to_country.csv')) as csv_file:
            reader = csv.reader(csv_file)
            country_code_to_country = dict(reader)
        geoip_data = geoip.GeoIP(os.path.join(data_directory, 'GeoIP.dat'))
        tracking = defaultdict(set)
        cursor = self.collections['tracking'].find()
        for item in cursor:
            username = item['username']
            if not username:
                username = 'unknown'
            ip = item['ip']
            if ip:
                tracking[username].add(ip)
        temp_result = []
        seen = set()
        for user, ips in tracking.iteritems():
            for ip in ips:
                try:
	            country_code = geoip_data.country(ip)
                    country = country_code_to_country[country_code]
                except KeyError:
                    # IMPORTANT
                    # The following code for an exception are hardcoded for those
                    # IPs which do have a mapping to a country code but they were
                    # not available in GeoIP.dat (most probably because it was
                    # not updated). People using this script can either report this
                    # code (under except) and or additional conditions IP addresses
                    # which cannot be mapped to a country code stored in GeoIP.dat
                    if ip == '41.79.120.29':
                        country_code = 'SS'
                        country = country_code_to_country['SS']
                    else:
                        print "Key Error Exception for IP {0}".format(ip)
                except Exception:
                    print "Uknown exception for ip {0}".format(ip)
                if (username, country) in seen:
                    continue
                if username != 'unknown':
                    seen.add((username, country))
                temp_result.append([username, ip, country_code, country])
        result = []
        for item in (a for a in temp_result):
            username = item[0]
            if username == 'unknown':
                user_id = 'unknown'
                hash_id = 'unknown'
            else:
                if username.isdigit():
                    username = int(username)
                user_id_map =  (self.collections['user_id_map']
                                .find_one({'username' : username}))
                if user_id_map:
                    user_id = user_id_map['id']
                    hash_id = user_id_map['hash_id']
                else:
                    user_id = 'unknown'
                    hash_id = 'unknown'
            row = self.anonymize_row([hash_id], [user_id, username],
                                     [item[1], item[2], item[3]])
            result.append(row)
	headers = self.anonymize_headers(['IP Address', 'Country Code',
                                          'Country'])
        report_name = self.report_name(self.db.name, self.basic_cmd)
	self.generate_csv(result, headers, report_name)
