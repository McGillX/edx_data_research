'''

Run the following query in mongo to take a look:

db.tracking.findOne({"event_type":"problem_check","event.problem_id":"i4x://McGillX/ATOC185x_2/problem/e60f566b9a9342ac9b8dd3f92296af41"})


we are after this value = {"event.submission.i4x-McGillX-ATOC185x_2-problem-e60f566b9a9342ac9b8dd3f92296af41_#_#.answer":""}



output = CSV(csv_data, ['Username'] + sub_problem_question_ids, output_file=db_name+'problem_answer.csv')


"event" : {
                "submission" : {
                        "i4x-McGillX-ATOC185x_2-problem-e60f566b9a9342ac9b8dd3f92296af41_8_1" : {
                                "input_type" : "checkboxgroup",
                                "question" : "",
                                "response_type" : "choiceresponse",
                                "answer" : [
                                        "Desktop computer"
                                ],
                                "variant" : "",
                                "correct" : true
                        },
                        "i4x-McGillX-ATOC185x_2-problem-e60f566b9a9342ac9b8dd3f92296af41_9_1" : {
                                "input_type" : "textline",
                                "question" : "",
                                "response_type" : "stringresponse",
                                "answer" : "",
                                "variant" : "",
                                "correct" : true
                        },
                        "i4x-McGillX-ATOC185x_2-problem-e60f566b9a9342ac9b8dd3f92296af41_6_1" : {
                                "input_type" : "checkboxgroup",
                                "question" : "",
                                "response_type" : "choiceresponse",
                                "answer" : [
                                        "Home",
                                        "Public place such as wireless hotspot (e.g., public library, café)"
                                ],
                                "variant" : "",
                                "correct" : false
                        },
                        "i4x-McGillX-ATOC185x_2-problem-e60f566b9a9342ac9b8dd3f92296af41_2_1" : {
                                "input_type" : "choicegroup",
                                "question" : "",
                                "response_type" : "multiplechoiceresponse",
                                "answer" : "edX web page",
                                "variant" : "",
                                "correct" : true
                        },
                        "i4x-McGillX-ATOC185x_2-problem-e60f566b9a9342ac9b8dd3f92296af41_7_1" : {
                                "input_type" : "textline",
                                "question" : "",
                                "response_type" : "stringresponse",
                                "answer" : "",
                                "variant" : "",
                                "correct" : true
                        },
                        "i4x-McGillX-ATOC185x_2-problem-e60f566b9a9342ac9b8dd3f92296af41_4_1" : {
                                "input_type" : "choicegroup",
                                "question" : "",
                                "response_type" : "multiplechoiceresponse",
                                "answer" : "4 - I really enjoyed it",
                                "variant" : "",
                                "correct" : true
                        },
                        "i4x-McGillX-ATOC185x_2-problem-e60f566b9a9342ac9b8dd3f92296af41_3_1" : {
                                "input_type" : "choicegroup",
                                "question" : "",
                                "response_type" : "multiplechoiceresponse",



'''
import csv
import sys

from base_edx import EdXConnection
from generate_csv_report import CSV

db_name = sys.argv[1]
# highest level of problem id
main_problem_id = sys.argv[2]
number_of_sub_problems = sys.argv[3]

connection = EdXConnection(db_name, 'tracking' )
collection = connection.get_access_to_collection()

main_problems = collection['tracking'].find({"event_type":"problem_check", "event.problem_id": main_problem_id })


    
    
output = CSV(csv_data, ['Username'] + sub_problem_ids, output_file=db_name+'problem_answer.csv')
output.generate_csv()
