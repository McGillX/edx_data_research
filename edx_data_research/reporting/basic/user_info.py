'''
This module will retrieve info about students registered in the course

'''

def user_info(edx_obj):
    edx_obj.collections = ['certificates_generatedcertificate', 'auth_userprofile','user_id_map']
    cursor = edx_obj.collections['auth_userprofile'].find()
    user_info_result = []
    for index in cursor:
        user_id = index['user_id']
        try:
            final_grade = edx_obj.collections['certificates_generatedcertificate'].find_one({'user_id' : user_id})['grade']
            username = edx_obj.collections['user_id_map'].find_one({'id' : user_id})['username']
            user_info_result.append([user_id, index['name'], final_grade, username, index['gender'], index['year_of_birth'], index['level_of_education'], index['country'], index['city']])
        except:
            print "Exception occurred for user_id {0}".format(user_id)
    edx_obj.generate_csv(user_info_result, ['User ID','Name', 'Final Grade', 'Username', 'Gender', 'Year of Birth', 'Level of Education', 'Country', 'City'], output_file=edx_obj.db.name+'_user_info.csv')
