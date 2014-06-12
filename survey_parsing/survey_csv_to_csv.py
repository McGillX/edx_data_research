'''
Parse the edX csv entrance and exit surveys into a more readable csv format
'''

import csv, json, collections

# SPECIFY csv input filepath
CSV_FILENAME = "data/ExitPage2.csv"

# SPECIFY csv output file
CSV_OUTPUT_FILENAME = CSV_FILENAME.replace(".csv","_PARSED.csv")

# file hander
csv_read = csv.reader(open(CSV_FILENAME,'rb'))

# skip header
next(csv_read, None)

header_dict = {}

error_count = 0

for line in csv_read:
  try:
    state_dict = json.loads(line[1])
  except:
    error_count += 1
    continue
  if 'student_answers' in state_dict:
    for key in state_dict['student_answers']:
      if key not in header_dict:
        header_dict[key] = {}
      if type(state_dict['student_answers'][key]) is list:
        for s in state_dict['student_answers'][key]:
          if s not in header_dict[key]:
            header_dict[key][s] = {}
      elif 'choice_' in state_dict['student_answers'][key] and state_dict['student_answers'][key] not in header_dict[key]:
        header_dict[key][state_dict['student_answers'][key]] = {}

print str(error_count) + ' errors'

# def sort_dict(mydict):
#   mydict = collections.OrderedDict(sorted(mydict.items()))
#   for key in mydict:
#     if type(mydict[key]) is dict and len(mydict[key])>1:
#       mydict[key] = sort_dict(mydict[key])
#   return mydict

# def sort_dict(mydict):
#   sorted_dict = collections.OrderedDict()
#   for key in sorted(mydict): 
#     sorted_dict[key] = sort_dict(mydict[key])
#   return sorted_dict

# def number_dict(mydict,count):
#   for key in mydict:
#     if type(mydict[key]) is collections.OrderedDict and len(mydict[key])>0:
#       mydict[key],count = number_dict(mydict[key],count)
#     else:
#       mydict[key] = count
#       count += 1
#   return mydict,count

def number_sort_dict_to_array(mydict,myarray,count):
  for key in sorted(mydict):
    count+=1
    myarray.append(key)
    if type(mydict[key]) is dict and len(mydict[key])>0:
      mydict[key],myarray,count = number_sort_dict_to_array(mydict[key],myarray,count)
    else:
      mydict[key] = count
  return mydict,myarray,count

# def plug_values_into_array(state_dict,header_dict,myarray):
#   for key in state_dict:
#     if type(state_dict[key]) is dict:
#       myarray = plug_values_into_array(state_dict[key],header_dict[key],myarray[:])
#     elif type(state_dict[key]) is list:
#       for s in state_dict[key]:
#         myarray[header_dict[key][s]] = 1
#     elif type(state_dict[key]) is unicode and 'choice_' in state_dict[key]:
#       myarray[header_dict[key]] = 1
#     else:
#       myarray[header_dict[key]] = state_dict[key]
#   return myarray

header_array = ['username']
header_dict,header_array,count = number_sort_dict_to_array(header_dict,header_array,len(header_array)-1)

# file handers
csv_read = csv.reader(open(CSV_FILENAME,'rb'))
csv_writer = csv.writer(open(CSV_OUTPUT_FILENAME,'w+'))

# skip header
next(csv_read, None)
# write header
csv_writer.writerow(header_array)

template_array = [None for x in range(len(header_array)+1)]

for line in csv_read:
  try:
    state_dict = json.loads(line[1])
  except:
    continue
  if 'student_answers' in state_dict:
    write_array = template_array[:]
    write_array[0] = line[0]
    for key in state_dict['student_answers']:
      # case sentence not choice
      if type(header_dict[key]) is int:
        write_array[header_dict[key]] = state_dict['student_answers'][key].encode('utf-8','ignore')
      # case list of choices
      elif type(state_dict['student_answers'][key]) is list and type(header_dict[key]) is dict:
        for s in state_dict['student_answers'][key]:
          write_array[header_dict[key][s]] = 1
      # case one choice not list
      elif type(state_dict['student_answers'][key]) is unicode and type(header_dict[key]) is dict:
        write_array[header_dict[key][state_dict['student_answers'][key]]] = 1
    csv_writer.writerow(write_array)

print header_dict
