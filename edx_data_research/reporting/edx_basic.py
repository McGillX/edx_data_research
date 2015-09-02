from edx_data_research.reporting.edx_base import EdX

class Basic(EdX):

    def user_info(self):
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
                row = ([hash_id] if self.anonymize else
                       [hash_id, user_id, username, item['name']])
                row.extend([final_grade, item['gender'], item['year_of_birth'],
                            item['level_of_education'], item['country'],
                            item['city'], enrollment_date])
                result.append(row)
            except KeyError:
                print "Exception occurred for user_id {0}".format(user_id)
        headers = (['User Hash ID'] if self.anonymize else
                   ['User Hash ID', 'User ID', 'Username', 'Name'])
        headers.extend(['Final Grade', 'Gender', 'Year of Birth',
                        'Level of Education', 'Country', 'City', 'Enrollment Date'])
        self.generate_csv(result, headers, self.report_name(self.db.name,
                         __name__.split('.')[-1]))
