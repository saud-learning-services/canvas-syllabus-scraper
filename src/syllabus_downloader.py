"""
SYLLABUS_SEARCH: main

This file is responsible for everything.

authors:
@alisonmyers
@author: jeremyh2
"""

from helpers import get_user_inputs, get_syllabus_info, format_course_code
from termcolor import cprint
from canvasapi import Canvas
from util import shut_down
from shutil import rmtree
import pandas as pd
import requests
import pprint
import json
import os
import re
import csv
import urllib.request

# for printing neatly formatted objects (used for debugging)
pp = pprint.PrettyPrinter(indent=4)

def get_course_info(c, canvas, auth_header):
        try:
            this_course = {'name': c.name,
                'id': c.id,
                'course_code': c.course_code,
                'term': c.term['name'],
                'workflow_state': c.workflow_state,
                'syllabus_body': c.syllabus_body,
                'course_name_formatted': format_course_code(c.course_code),
                'extract_details': ''}
            course_name_formatted = this_course['course_name_formatted']
            msgs = get_syllabus_info(c, canvas, auth_header, this_course['term'], course_name_formatted)
            this_course['extract_details'] = msgs
            print(msgs)
            return(this_course)
            
        except Exception as e:
            cprint(f'{e}: Error getting data for {c.name}', 'red')


def main():
    # get user inputs
    canvas, account, auth_header, term = get_user_inputs()

    # get list of courses
    courses = account.get_courses(include=["term", "syllabus_body"])
    #courses = courses[0:10]
    course_data = []

   # total = courses.totalCount()
    
    for count, c in enumerate(courses, 1):

        try: 
            #TODO seperate the count from the function
            #TODO add overall counter i.e .1/X
            if c.term['name'].startswith(term):
                cprint(f"{count}: Getting data for {c.name}", 'green')
                try:
                    this_course = get_course_info(c, canvas, auth_header)
                    course_data.append(this_course)
                except Exception as e:
                    cprint(f'{count}: Unknown Error - {c.name}', 'red')
        
        except Exception as e:
            cprint(f'{e} ...', 'red')
    try:
        df = pd.DataFrame(course_data)
        df.to_csv(f"{term}-syllabus_download-tracking.csv")
    except Exception as e:
            cprint(f'Error in csv creation {e} ...')

if __name__ == "__main__":
    # execute only if run as a script
    main()