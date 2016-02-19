import json

from edx_data_research.parsing.parse import Parse

class CourseStructure(Parse):

    def __init__(self, args):
        super(CourseStructure, self).__init__(args)
        self.collections = ['course_structure']
        self.course_structure_file = args.course_structure_file
        self.drop = args.drop
    
    def migrate(self):
        if self.drop:
            self.collections['course_structure'].drop()
        json_data = self._load_json_data(self.course_structure_file)
        json_data = self._parse_key_names(json_data)
        json_data = self._delete_category(json_data, 'conditional')
        json_data = self._delete_category(json_data, 'wrapper')
        json_data = self._build_parent_data(json_data)
        json_data = self._update_parent_data(json_data)
        for key in json_data:
            self.collections['course_structure'].insert(json_data[key])
    
    def _load_json_data(self, file_name):
        '''Retrieve data from the json file'''
        with open(file_name) as file_handler:
            json_data = json.load(file_handler)
        return json_data
    
    def _parse_key_names(self, json_data):
        '''Parse key names'''
        new_json_data = {}
        for key in json_data:
            new_key = key.split('/')[-1]
            json_data[key]['_id'] = new_key
            if json_data[key]['children']:
                for index, child in enumerate(json_data[key]['children']):
                    json_data[key]['children'][index] = child.split('/')[-1]
            new_json_data[new_key] = json_data[key]
        return new_json_data
    
    def _delete_category(self, json_data, category):
        '''Delete data with given category from json_data '''
        for key in json_data.keys():
            if json_data[key]['category'] == category:
                for item in json_data.keys():
                    if json_data[item]['children'] and key in json_data[item]['children']:
                        parent_id = item
                index_child = json_data[parent_id]['children'].index(key)
                left_list = json_data[parent_id]['children'][:index_child]
                right_list = json_data[parent_id]['children'][index_child + 1:]
                json_data[parent_id]['children'] = left_list + json_data[key]['children'] + right_list
                del json_data[key]
        return json_data
    
    def _build_parent_data(self, json_data):
        '''Build parent data'''
        error_count = 0
        for key in json_data:
            if json_data[key]['children']:
                for index, child_key in enumerate(json_data[key]['children']):
                    try:
                        json_data[child_key]['parent_data'] = {}
                    except:
                        error_count += 1
                        continue
                    parent_category = json_data[key]['category']
                    parent_order_key = parent_category + '_order'
                    parent_id_key = parent_category + '_id'
                    parent_display_name_key = parent_category + '_display_name'
                    json_data[child_key]['parent_data'][parent_order_key] = index
                    json_data[child_key]['parent_data'][parent_id_key] = json_data[key]['_id']
                    json_data[child_key]['parent_data'][parent_display_name_key] = json_data[key]['metadata']['display_name']
        print "Number of errors when building parent data: {0}".format(error_count)
        return json_data
    
    def _update_parent_data(self, json_data):
        for key in json_data:
            if json_data[key]['category'] == 'sequential':
                chapter_id = json_data[key]['parent_data']['chapter_id']
                chapter_parent_data = json_data[chapter_id]['parent_data']
                json_data[key]['parent_data'].update(chapter_parent_data)
    
        for key in json_data:
            if json_data[key]['category'] == 'vertical':
                sequential_id = json_data[key]['parent_data']['sequential_id']
                sequential_parent_data = json_data[sequential_id]['parent_data']
                json_data[key]['parent_data'].update(sequential_parent_data)
    
        for key in json_data:
            if json_data[key]['category'] not in set(['vertical', 'sequential', 'chapter', 'course']):
                try:
                    vertical_id = json_data[key]['parent_data']['vertical_id']
                    vertical_parent_data = json_data[vertical_id]['parent_data']
                    json_data[key]['parent_data'].update(vertical_parent_data)
                except:
                    print "ERROR: {0}".format(json_data[key])
        return json_data
