'''
This module was created to try to do sentiment analysis on a discussion
debationg whether multivitamins should be used or not. The data came from
the edX discussion board comments of CHEM181x. 

Reference code for the sentiment analysis was taken from: 
https://github.com/abromberg/sentiment_analysis_python
For documentation, check out the blog post about this code [here](http://andybromberg.com/sentiment-analysis-python)

The refernece code, specifically sentiment_analysis.py  was modified
to our requirements.

Current code is incomplete as out of 1200 comments , only 100 were manually 
tagged as positive, negative or neutral. Of these 100 comments, 70 were using for 
training the classifier and 30 were for test data on which classifier was used. Based
on this training and test data, the accuracy of the classifier came to 40%. The main 
reason for this is because a very small dataset (100 out of 1200) was used for training and 
testing the classifier. If this number could be increased to 300 (i.e. 300 of the comments 
were manually tagged), the accuracy could be improved
  
'''

import nltk
from nltk.corpus import stopwords
import re
import random
import csv
import json

import sentiment_analysis

with open('multivitamin_debate_data.csv') as f:
    reader = csv.reader(f)
    reader.next()
    tagged_comments = [tuple(row) for row in reader]
    num_of_none = sum(1 for row in tagged_comments if row[1] == 'none')
    num_of_neg = sum(1 for row in tagged_comments if row[1] == 'neg')
    print num_of_none, num_of_neg
with open('data.json') as f:
    discussion = json.load(f)
#print len(discussion), type(discussion)

classifier = sentiment_analysis.evaluate_features(sentiment_analysis.make_full_dict, tagged_comments)

#discussion_features = {}  
#for i in discussion:
#    words = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
#    #words = sentiment_analysis.make_full_dict(words)
#    discussion_features[i] = words

#predicted = [(j,classifier.classify(i)) for j in discussion_features for i in discussion_features[j]]
#predicted = [(j,classifier.classify(discussion_features[j])) for j in discussion_features ]
#for item in predicted:
#    print item
#print len(predicted)

#classifier = sentiment_analysis.evaluate_features(sentiment_analysis.make_full_dict)
# Using 10000 most informative words
# classifier, accuracy = sentiment_analysis.evaluate_features(sentiment_analysis.best_word_features)

def get_stats(predicted):
    agree = sum(1 for item in predicted if item[1] == 'pos')
    disagree = sum(1 for item in predicted if item[1] == 'neg')
    return agree * 100.0 /len(predicted), disagree * 100.0 / len(predicted) 

#print "Classifier Accuracy: ", accuracy * 100
#stats = get_stats(predicted)
#print "Agree: ", stats[0]
#print "Disagree: ",stats[1]
