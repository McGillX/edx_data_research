import csv
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib

from generate_csv_report import CSV

with open(sys.argv[1], 'r') as csv_file:
    reader = csv.reader(csv_file)
    reader.next()
    #data = [row for row in reader if row[3] and int(row[3]) > int(row[4])]
    data = defaultdict(float)
    for row in reader:
        if row[3] and int(row[3]) > int(row[4]):
            data[(row[0],row[1],row[3],row[4])] += float(row[5])

data_output = [[row[0], row[1],row[2],row[3], data[row], int(row[3]) - int(row[2]) ] for row in data]
output = CSV(data_output, ['Chapter Name', 'Sequential Name', 'Event Old', 'Event New', 'Count', 'Distance'], output_file='sequence_back_analysis.csv')
output.generate_csv()