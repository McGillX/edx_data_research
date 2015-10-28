from edx_data_research.parsing.edx_parse import EdXParse

class ProblemIds(EdXParse):

    def __init__(self, args):
        super(ProblemIdsCollection, self).__init__(args)
        
    def migrate(self):
        self.collections = ['problem_ids', 'tracking', 'user_id_map']
        self.collections['problem_ids'].drop()
        tracking_cursor = (self.collections['tracking']
    			   .find({'event_type' : 'problem_check',
                           'event_source' : 'server'}))
        for item in cursor:
            document = {}
            username = document['username']
	    try:
                username = int(username)
	    except ValueError:
		pass
            document['username'] = username
            user_id_map = (self.collections['user_id_map']
                           .find_one({'username' : username}))
            if not user_id_map:
		print "Username {0} not found in collection user_id_map".format(username)
                continue
	    document['user_id'] = user_id_map['id']
	    document['hash_id'] = user_id_map['hash_id']
            document['problem_id'] = item['event']['problem_id'] 
            document['course_id'] = item['context']['course_id'] 
            document['module'] = item['context']['module'] 
            document['time'] = item['time'] 
            document['event'] = item['event']
	    self.collections['problem_ids'].insert(document) 
            
