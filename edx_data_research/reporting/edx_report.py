import csv
import os

from edx_data_research.edx_base import EdX

class EdXReport(EdX):

    def __init__(self, args):
        client = MongoClient(self.uri)
        self.db = client[self.db_name]
        self.output_directory = args.output_directory
        self.row_limit = args.row_limit
        self.csv_data = None
        self.headers = None
        self.anonymize = args.anonymize
        
    def generate_csv(self, csv_data, headers, output_file):
    	"""
    	Genersate csv report from generated data and given list of headers
    	"""
        self.csv_data = csv_data
        self.headers = headers
        number_of_data_points = len(self.csv_data)
        if number_of_data_points < self.row_limit:
            number_of_rows = self._write_to_csv(output_file)
            return number_of_rows == number_of_data_points + 1
        number_of_splits = number_of_data_points // self.row_limit
        if number_of_data_points % self.row_limit:
            number_of_splits += 1
        number_of_rows = sum([self._write_to_csv(output_file.split('.')[0] +
                              '_' + str(index) + '.csv', index)
                              for index in xrange(number_of_splits)])
        return number_of_rows == number_of_data_points + number_of_splits
	        
    def _write_to_csv(self, output_file, index=0):
    	"""
    	Helper method to write rows to csv files
    	"""
    	output_file_path = os.path.abspath(os.path.join(self.output_directory,
                                           output_file))
        with open(output_file_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.headers)
            row_count = 1
            for row in (item for item in self.csv_data[index * self.row_limit :
                       (index + 1) * self.row_limit]):
                # This loop looks for unicode objects and encodes them to 
                # ASCII to avoid Unicode errors, for e.g. UnicodeEncodeError: 
                # 'ascii' codec can't encode character u'\xf1'
                row = [item.encode('ascii', 'ignore')  if isinstance(item, unicode)
                       else item for item in row]
                writer.writerow(row)
		row_count += 1
        return row_count

    def report_name(self, *args):
        return '-'.join(item for item in args) + '.csv'

    def anonymize_row(self, yes, no, rest):
        row = yes if self.anonymize else yes + no
        row.extend(rest)
        return row

    def anonymize_headers(self, headers):
        return self.anonymize_row(['Hash ID'], ['User ID', 'Username'], headers)

    def user_map(self, user_id=None, username=None):
        if username:
            user_map = (self.collections['user_id_map']
                        .find_one({'username' : username}))
            return ((user_map['hash_id'], user_map['id']) if user_map
                    else (None, None))
        user_map = (self.collections['user_id_map']
                    .find_one({'id' : user_id}))
        return ((user_map['hash_id'], user_map['username']) if user_map
                else (None, None))
