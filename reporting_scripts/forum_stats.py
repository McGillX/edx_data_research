'''
This module calculates the number of forum threads and posts for a given course
stored in the MongoDB database

Usage:

python <path_to_script> 

'''
from common.base_edx import EdXConnection

connection = EdXConnection('forum' )
collection = connection.get_access_to_collection()

# Number of documents with _type CommentThread
# A CommentThread represents the first level of interaction: a post that opens 
#a new thread, often a student question of some sort
number_of_comment_threads = collection['forum'].find({'_type' : 'CommentThread'}).count()

# Total number of comments in the forum
number_of_posts = collection['forum'].find().count()

print number_of_posts, number_of_comment_threads
