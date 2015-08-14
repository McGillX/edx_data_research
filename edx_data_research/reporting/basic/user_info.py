'''
This module will retrieve info about students registered in the course

'''

def user_info(edx_obj):
    edx_obj.collections = ['certificates_generatedcertificate', 'auth_userprofile','user_id_map','student_courseenrollment']
    cursor = edx_obj.collections['auth_userprofile'].find()
    result = []
    for item  in cursor:
        user_id = item['user_id']
        try:
            final_grade = edx_obj.collections['certificates_generatedcertificate'].find_one({'user_id' : user_id})['grade']
            username = edx_obj.collections['user_id_map'].find_one({'id' : user_id})['username']
            enrollment_date = edx_obj.collections['student_courseenrollment'].find_one({'user_id' : user_id})['created']
            result.append([user_id, item['name'], final_grade, username, item['gender'], item['year_of_birth'], item['level_of_education'], item['country'], item['city'], enrollment_date])
        except:
            print "Exception occurred for user_id {0}".format(user_id)
    edx_obj.generate_csv(result, ['User ID','Name', 'Final Grade', 'Username', 'Gender', 'Year of Birth', 'Level of Education', 'Country', 'City','Enrollment Date'], output_file=edx_obj.db.name+'_user_info.csv')
