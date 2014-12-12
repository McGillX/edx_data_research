'''
In this module, we insert the course structure provided by edX as a json file
into the mongodb database
The one JSON object will be split into sub objects, in which all the first level
keys will become the _id of its object value

'''

import pymongo
import json
import sys 


def connect_to_db_collection(db_name, collection_name):
    '''
    Retrieve collection from given database name and collection name

    '''
    connection = pymongo.Connection('localhost', 27017)
    db = connection[db_name]
    collection = db[collection_name]
    return collection


def get_json_data(file_name):
    '''
    Retrieve data from the json file

    '''
    with open(file_name) as file_handler:
        json_data = json.load(file_handler)
    return json_data


def parse_key_names(json_data):
    '''
    Parse key names

    '''
    new_json_data = {}
    for key in json_data:
        new_key = key.split('/')[-1]
        json_data[key]['_id'] = new_key
        if json[key]['children']:
            for index, child in enumerate(json_data[key]['children']):
                json_data[key]['children'][index] = child.split('/')[-1]
        new_json_data[new_key] = json_data[key]
    return new_json_data


def delete_category(json_data, category):
    '''
    Delete data with given category from json_data 

    '''
    key_to_delete = []
    for key in json_data.keys():
        if json_data[key]['category'] == category:
            for item in json_data.keys():
                if json_data[item]['children'] and key in json_data[item]['children']:
                    parent_id = item
            index_child = json[parent_id]['children'].index(key)
            left_list = json_data[parent_id]['children'][:index_child]
            right_list = json_data[parent_id]['children'] = left_list + json_data[key]['children'] + right_list
            del json_data[key]
    return json_data


def build_parent_data(json_data):
    '''
    Build parent data

    '''
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
    print "Number of errors when building parent data: ", error_count
    return json_data


def update_parent_data(json_data):
    for key in json_data[key]:
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
        if json_data[key]['category'] not in set(['vertical', 'sequential', 'chapter', 'course'])
            try:
                vertical_id = json_data[key]['parent_data']['vertical_id']
                vertical_parent_data = json_data[vertical_id]['parent_data']
                json_data[key]['parent_data'].update(vertical_parent_data)
            except:
                print "ERROR: ", json_data[key]
    return json_data


def main():
    if len(sys.argv) != 4:
        usage_message = 'usage: %s db collection json_file'
        sys.stderr.write(usage_message % sys.argv[0])
        sys.exit(1)

    json_data = get_json_data(sys.argv[3])
    json_data = parse_key_names(json_data)
    json_data = delete_category(json_data, 'conditional')
    json_data = delete_category(json_data, 'wrapper')
    json_data = build_parent_data(json_data)
    json_data = update_parent_data(json_data)
    collection = connect_to_db_collection(sys.argv[1], sys.argv[2])
    collection.insert(json_data)


if __name__ == '__main__':
    main()
