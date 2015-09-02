'''
This module retrieve info from the forum collection for a given course

'''
def forum(edx_obj):
    edx_obj.collections = ['forum']
    cursor = edx_obj.collections['forum'].find()
    result = [[document['_id'], document['author_username'], document['_type'],
              document.get('title', ''), document['body'],
              document['created_at']] for document in cursor]
    headers = ['ID', 'Author Username', 'Type', 'Title', 'Body', 'Created At Date']
    edx_obj.generate_csv(result, headers, edx_obj.report_name(edx_obj.db.name,
                         __name__.split('.')[-1]))
