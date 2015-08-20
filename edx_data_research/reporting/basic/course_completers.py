'''
This module extracts the student IDs from the collection
certificates_generatedcertificate of the students who completed the course and
achieved a certificate. The ids are then used to extract the usernames of the
course completers

'''

def course_completers(edx_obj):
    edx_obj.collections = ['certificates_generatedcertificate', 'auth_user']
    cursor = (edx_obj.collections['certificates_generatedcertificate']
              .find({'status' : 'downloadable'}))
    result = []
    for item in cursor:
        user_document = (edx_obj.collections['auth_user']
                        .find_one({"id" : item['user_id']}))
        result.append([user_document['id'], user_document['username'],
                       item['name'], item['grade']])
    edx_obj.generate_csv(result, ['User ID','Username', 'Name', 'Grade'],
                         output_file=edx_obj.db.name+'_course_completers.csv')
