'''
Convert the edx .mongo format to a conventional .json format
'''

# SPECIFY input .mongo filename
mongo_filename = 'McGillX-CHEM181x-1T2014-prod.mongo'

# SPECIFY output .json filename
json_filename = mongo_filename.replace('.mongo','.json')

# input file handler
mongo_file = open(mongo_filename,"r")

# output file handler
json_file = open(json_filename,"w+")

json_file.write('[')

for row in mongo_file.readlines():
  row = row.replace('\n','')
  json_file.write(row+','+'\n')

json_file.write(']')

mongo_file.close()
json_file.close()