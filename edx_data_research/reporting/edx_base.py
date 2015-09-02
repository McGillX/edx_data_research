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
        self.list_of_headers = None
        self.anonymize = args.anonymize
        
    def generate_csv(self, csv_data, list_of_headers, output_file):
    	"""
    	Genersate csv report from generated data and given list of headers
    	"""
    	self.csv_data = csv_data
    	self.list_of_headers = list_of_headers
    	number_of_rows = len(csv_data) + 1
        if number_of_rows <= self.row_limit:
	        self._write_to_csv(output_file)
        else:
	        if number_of_rows % self.row_limit:
		        number_of_splits = number_of_rows // self.row_limit + 1
	        else:
		        number_of_splits = number_of_rows // self.row_limit
	        for index in xrange(number_of_splits):
	            self._write_to_csv(output_file.split('.')[0] + '_' + str(index) + '.csv', index)
	        
    def _write_to_csv(self, output_file, number_of_splits=0):
    	"""
    	Helper method to write rows to csv files
    	"""
    	output_file_path = os.path.abspath(os.path.join(self.output_directory, output_file))
        with open(output_file_path, 'w') as csv_file:
	        writer = csv.writer(csv_file)
	        writer.writerow(self.list_of_headers)
	        for row in self.csv_data[number_of_splits * self.row_limit : (number_of_splits + 1) * self.row_limit]:
	            # This loop looks for unicode objects and encodes them to ASCII to avoif Unicode errors,
		        # for e.g. UnicodeEncodeError: 'ascii' codec can't encode character u'\xf1'
		        for index,item in enumerate(row[:]):
		            if isinstance(item, unicode):
		                row[index] = item.encode('ascii', 'ignore')
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
