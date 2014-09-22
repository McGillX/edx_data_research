'''
This module generates a csv report based on given csv_data, which will be a 2D array, and the list of list_of_headers
If the data is very big, this module will split the data into a number of csv files. E.g. if the 2D data has 10200 
rows, and user wants csv file to have only 5000 rows, then this module would split it into 3 csv files with 5000, 5000
and 200 rows

The CSV constructor has 2 required parameters: csv_data and list_of_headers and 2 optional parameters: output_file
and row_limit. 

Usage:

from generate_csv_report import CSV
# data should be in the format of 2D array or list of lists
output = CSV(data, ['Header 1', 'Header 2', 'Header 3', 'Header 4'], output_file='name_of_output_file.csv')
output.generate_csv()



'''

import csv
from collections import defaultdict

class CSV(object):

	def __init__(self, csv_data, list_of_headers, output_file='output.csv', row_limit=100000):
		self.csv_data = csv_data
		self.output_file = output_file
		self.list_of_headers = list_of_headers
		self.output_file = output_file
		self.row_limit = row_limit

	def generate_csv(self):
		if len(self) <= self.row_limit:
			self._write_to_csv(self.output_file)
		else:
			if len(self) % self.row_limit:
				number_of_splits = len(self) // self.row_limit + 1
			else:
				number_of_splits = len(self) // self.row_limit
			for index in xrange(number_of_splits):
				self._write_to_csv(self.output_file.split('.')[0] + '_' + str(index) + '.csv', index)					

	def _write_to_csv(self, output_file, number_of_splits=0):
		with open(output_file, 'w') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(self.list_of_headers)
			for row in self.csv_data[number_of_splits * self.row_limit : (number_of_splits + 1) * self.row_limit]:
				# This loop looks for unicode objects and encodes them to ASCII to avoif Unicode errors,
				# for e.g. UnicodeEncodeError: 'ascii' codec can't encode character u'\xf1'
				for index,item in enumerate(row[:]):
				    if type(item) is unicode:
					row[index] = item.encode('ascii', 'ignore')
				writer.writerow(row)

	def __len__(self):
		return len(self.csv_data) + 1
