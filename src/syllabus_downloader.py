"""
SYLLABUS_SEARCH: main

This file is responsible for everything.

authors:
@alisonmyers
@markoprodanovic

This adapatation was forked from https://github.com/ubccapico/syllabus-scraper where the original authors are:

Original Authors
Jeremy Hidjaja - @JeremyH011
Barish Golland - @barishgolland
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

ENROLLMENT_TERMS = {}

# for printing neatly formatted objects (used for debugging)
pp = pprint.PrettyPrinter(indent=4)


def get_course_info(c, canvas, auth_header):
    try:
        this_course = {
            "name": c.name,
            "id": c.id,
            "course_code": c.course_code,
            "term": c.term["name"],
            "workflow_state": c.workflow_state,
            "syllabus_body": c.syllabus_body,
            "course_name_formatted": format_course_code(c.course_code),
            "extract_details": "",
        }
        course_name_formatted = this_course["course_name_formatted"]
        msgs = get_syllabus_info(
            c, canvas, auth_header, this_course["term"], course_name_formatted
        )
        this_course["extract_details"] = msgs
        print(msgs)
        return this_course

    except Exception as e:
        cprint(f"{e}: Error getting data for {c.name}", "red")


def filter_to_term(courses, term):
    """
    args:
        courses (Pagniated list type course): Courses to filter through
        term (string): ex. "2017W2"
    """

    count = 0
    term_courses = []

    for c in courses:
        if c.term["name"].startswith(term):
            term_courses.append(c)
            count += 1

    return term_courses, count


def main():
    # get user inputs
    canvas, account, auth_header, term = get_user_inputs()

    cprint(f"\nQuerying courses in {account.name}...\n", "yellow")

    # get list of courses
    courses = account.get_courses(include=["term", "syllabus_body"])
    course_data = []

    # term_courses is a list, not PaginatedList
    # course count is the number of courses that match that term id
    term_courses, total_course_count = filter_to_term(courses, term)

    # COUNT COURSES BY TRAVERSING THE PAGINATED LIST
    # total = courses.totalCount()

    for count, c in enumerate(term_courses, 1):

        try:
            if c.term["name"].startswith(term):
                cprint(
                    f"\n{count}: Getting data for {c.name} [{count}/{total_course_count}]",
                    "green",
                )
                try:
                    this_course = get_course_info(c, canvas, auth_header)
                    course_data.append(this_course)
                except Exception as e:
                    cprint(f"{count}: Error getting course info - {c.name}", "red")

        except Exception as e:
            cprint(f"Unresolved error\n:{e} ...\n", "red")
    try:
        df = pd.DataFrame(course_data)
        df.to_csv(f"{term}-syllabus_download-tracking.csv")
    except Exception as e:
        cprint(f"Unknown error in csv creation\n{e}\n...")


if __name__ == "__main__":
    # execute only if run as a script
    main()
