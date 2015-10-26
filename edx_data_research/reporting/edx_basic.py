import csv
import os

from collections import defaultdict, namedtuple

from edx_data_research.reporting.edx_base import EdXReport
from edx_data_research.reporting.lib import geoip

class Basic(EdXReport):

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
                hash_id, username = self.user_map(user_id=user_id)
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
        report_name = self.report_name(self.db_name, self.basic_cmd)
        self.generate_csv(result, headers, report_name)

    def course_completers(self):
        '''
        Extract the student IDs from the collection
        certificates_generatedcertificate of the students who completed the
        course and achieved a certificate. The ids are then used to extract
        the usernames of the course completers
        '''
        self.collections = ['certificates_generatedcertificate', 'user_id_map']
        cursor = (self.collections['certificates_generatedcertificate']
                  .find({'status' : 'downloadable'}))
        result = []
        for item in cursor:
            user_id = item['user_id']
            hash_id, username = self.user_map(user_id=user_id)
            row = self.anonymize_row([hash_id],
                                     [user_id, username],
                                     [item['name'], item['grade']])
            result.append(row)
        headers = self.anonymize_headers(['Name', 'Grade'])
        report_name = self.report_name(self.db_name, self.basic_cmd)
        self.generate_csv(result, headers, report_name)

    def forum(self):
        '''Retrieve info from the forum collection for a given course'''
        self.collections = ['forum', 'user_id_map']
        cursor = self.collections['forum'].find()
        result = []
        for item in cursor:
            user_id = int(item['author_id'])
            hash_id, _ = self.user_map(user_id=user_id)
            row = self.anonymize_row([hash_id],
                                     [user_id, item['author_username']],
                                     [item['_type'], item.get('title', ''),
                                      item['body'], item['created_at']])
            result.append(row)
        headers = self.anonymize_headers(['Type', 'Title', 'Body',
                                          'Created At Date'])
        report_name = self.report_name(self.db_name, self.basic_cmd)
	self.generate_csv(result, headers, report_name)

    def ip_to_country(self):
        '''Map user's IP address to a country'''
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
                hash_id, user_id = 'unknown', 'unknown'
            else:
                if username.isdigit():
                    username = int(username)
                hash_id, user_id = self.user_map(username=username)
                if not (hash_id and user_id):
                    hash_id, user_id = 'unknown', 'unknown'
            row = self.anonymize_row([hash_id], [user_id, username],
                                     [item[1], item[2], item[3]])
            result.append(row)
	headers = self.anonymize_headers(['IP Address', 'Country Code',
                                          'Country'])
        report_name = self.report_name(self.db_name, self.basic_cmd)
	self.generate_csv(result, headers, report_name)

    def date_of_registration(self):
        '''Retrieve date of registration of students'''
        self.collections = ['student_courseenrollment', 'user_id_map']
        cursor = self.collections['student_courseenrollment'].find()
        seen = set()
        result = []
        for item in cursor:
            user_id = item['user_id']
            if user_id not in seen:
                seen.add(user_id)
                hash_id, username = self.user_map(user_id=user_id)
                row = self.anonymize_row([hash_id], [user_id, username],
                                         [item['created'].split()[0]])
                result.append(row)
        headers = self.anonymize_headers(['Date of Registration'])
        report_name = self.report_name(self.db_name, self.basic_cmd)
        self.generate_csv(result, headers, report_name)

    def sequential_aggregation(self):
        '''
        Retrieve the number of various categories under each sequential in 
        the collection course_structure
        '''
        self.collections = ['course_structure']
        cursor = (self.collections['course_structure']
                  .find({'category' : 'sequential'}))
        result = []
        for item in cursor:
            children = item['children']
            aggregate_vertical = defaultdict(int)
            aggregate_category = defaultdict(int)
            for child_id in children:
                child = (self.collections['course_structure']
                         .find_one({'_id' : child_id}))
                aggregate_vertical[child['category']] += 1
                for grand_child_id in child['children']:
                    grand_child = (self.collections['course_structure']
                                   .find_one({'_id' : grand_child_id}))
                    aggregate_category[grand_child['category']] += 1
            result.append([item['_id'],
                           item['parent_data']['chapter_display_name'],
                           item['metadata']['display_name'], len(children),
                           aggregate_category['video'],
                           aggregate_category['html'],
                           aggregate_category['problem'],
                           aggregate_category['discussion'],
                           aggregate_category['poll_question'],
                           aggregate_category['word_cloud']])
        headers = ['Sequential ID', 'Chapter Display Name', 'Sequential Name',
                   'Number of Verticals', 'Number of Videos', 'Number of HTMLs',
                   'Number of Problems' ,'Number of Discussions',
                   'Number of Poll Questions', 'Number of Word Clouds']
        report_name = self.report_name(self.db_name, self.basic_cmd)
        self.generate_csv(result, headers, report_name)
