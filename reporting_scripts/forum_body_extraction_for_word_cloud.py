'''
This module extracts all of the comments and comment threads from the forum of 
a given course. Using NLTK, all of the comments and comment threads will be 
parsed into a list of words which will be then used to create a word cloud 
using http://www.wordle.net/create 

Usage:

python forum_body_extraction_for_word_cloud.py > word_cloud.txt

The above command would get the top 1000 words and print those words the
number of times they were used and the result is outputted to a text file,
e.g. word_cloud.txt. User can copy the text in word_cloud.txt and paste in
http://www.wordle.net/create to generate the word cloud

'''

import nltk
from nltk.corpus import stopwords
import json
import heapq

from base_edx import EdXConnection
from generate_csv_report import CSV

connection = EdXConnection('forum')
collection = connection.get_access_to_collection()

cursor = collection['forum'].find()
body_data = [item['body'] for item in cursor]
# Words that are not required to be considered in the word cloud can be added
# to the list ignore_words. If user would like to pass this list via command
# line, the user can do the following:
# import sys
# ignore_word = sys.argv[1]
# where sys.argv[1] is of the format ['http', 'https'] and usage becomes:
# python forum_body_extraction_for_word_cloud.py list_of_ignore_words > word_cloud.txt
ignore_words = ['http', 'https']
tokens = []
for item in body_data:
    words = []
    for word in nltk.word_tokenize(item):
        clean_word = word.lower().encode('utf-8').strip('\'\"\-,.:;!?()[]{}=#*_$/%+&<>')
        if clean_word and clean_word not in stopwords.words('english') and len(clean_word) > 2 and '\'' not in clean_word and clean_word not in ignore_words:
            words.append(clean_word)
    tokens.extend(words)
fd = nltk.FreqDist(tokens)
top_1000 = heapq.nlargest(1000, fd, key=fd.get)
top_1000_list = []
for item in top_1000:
    top_1000_list.extend([str(item)] * fd[item])    
print ' '.join(top_1000_list)
