import csv
import os

from pymongo import MongoClient


class EdX(object):

    def __init__(self, args):
        self.uri = args.uri
        client = MongoClient(self.uri)
        self.db = client[args.db_name]
        self._collections = None
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
        number_of_rows = len(self.csv_data) + 1
        if number_of_rows <= self.row_limit:
	        self._write_to_csv(output_file)
        else:
	        if number_of_rows % self.row_limit:
		        number_of_splits = number_of_rows // self.row_limit + 1
	        else:
		        number_of_splits = number_of_rows // self.row_limit
	        for index in xrange(number_of_splits):
	            self._write_to_csv(output_file.split('.')[0] + '_' + str(index) + '.csv', index)
	        
    def _write_to_csv(self, output_file, index=0):
    	"""
    	Helper method to write rows to csv files
    	"""
    	output_file_path = os.path.abspath(os.path.join(self.output_directory, output_file))
        with open(output_file_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.headers)
            for row in (item for item in self.csv_data[index * self.row_limit :
                       (index + 1) * self.row_limit]):
                # This loop looks for unicode objects and encodes them to ASCII to avoif Unicode errors,
                # for e.g. UnicodeEncodeError: 'ascii' codec can't encode character u'\xf1'
                row = [item.encode('ascii', 'ignore')  if isinstance(item, unicode)
                       else item for item in row]
                writer.writerow(row)
		
    @property
    def collections(self):
    	return self._collections
    	
    @collections.setter
    def collections(self, _collections):
    	self._collections = {collection : self.db[collection] for collection in _collections}

    def report_name(self, *args):
        return '-'.join(item for item in args) + '.csv'

    def anonymize_row(self, yes, no, rest):
        row = yes if self.anonymize else yes + no
        row.extend(rest)
        return row

    def anonymize_headers(self, headers):
        return self.anonymize_row(['Hash ID'], ['User ID', 'Username'], headers)
