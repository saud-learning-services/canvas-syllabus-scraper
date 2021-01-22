import requests
import pandas as pd
import re
import sys
import os
import glob
import ast
from util import shut_down
import getpass
from canvasapi import Canvas
from termcolor import cprint
from bs4 import BeautifulSoup


def format_course_code(course_code):
    # Format course code for file saving
    #   takes a course code string
    #   returns: a formatted string
    # TODO - all characters not letters etc replaced with _ 
    course_code = course_code.replace(' ', '', 1)\
        .replace(' ', '_')\
        .replace('-', '_')\
        .replace('.', '_')
    return course_code


def get_user_inputs():
    """Prompt user for required inputs. Queries Canvas API throughout to check for
    access and validity errors. Errors stop execution and print to screen.

    Returns:
        Dictionary containing inputs
    """

    # prompt user for url and token
    url = "https://ubc.test.instructure.com/"
    # url = "https://canvas.ubc.ca/"
    token = input('Please enter your token: ')
    term = input('Please enter the Canvas term or year (or hit enter for all): ')
    auth_header = {'Authorization': f'Bearer {token}'}

    # Canvas object to provide access to Canvas API
    canvas = Canvas(url, token)

    # get user object
    try:
        user = canvas.get_user('self')
        cprint(f'\nHello, {user.name}!', 'green')
    except Exception:
        shut_down(
            """
            ERROR: could not get user from server.
            Please ensure token is correct and valid and ensure using the correct instance url.
            """
        )
    # get account object
    try:
        account_id = input('Account ID: ')
        account = canvas.get_account(account_id)
    except Exception:
        shut_down(
            f'ERROR: Account not found [ID: {account_id}]. Please check account number.'
        )


    # prompt user for confirmation
    _prompt_for_confirmation(user.name, account.name, term)

    # set course, quiz, students and auth_header as global variables

    # return inputs dictionary
    return canvas, account, auth_header, term 


def _prompt_for_confirmation(user_name, account_name, term):
    """Prints user inputs to screen and asks user to confirm. Shuts down if user inputs
    anything other than 'Y' or 'y'. Returns otherwise.

    Args:
        user_name (string): name of user (aka. holder of token)
        account_name (string): name of account returned from Canvas

    Returns:
        None -- returns only if user confirms

    """
    cprint('\nConfirmation:', 'blue')
    print(f'USER:  {user_name}')
    print(f'RUNNING ON ACCOUNT:  {account_name}')
    print(f'RUNNING FOR TERM:  {term}')
    print('\n')

    confirm = input(
        'Would you like to continue using the above information? [y/n]: ')

    print('\n')

    if confirm == 'y' or confirm == 'Y':
        return
    elif confirm == 'n' or confirm == 'N':
        shut_down('Exiting...')
    else:
        shut_down('ERROR: Only accepted values are y and n')



def get_syllabus_info(course, canvas, auth_header, year, name):
    s = course.syllabus_body 
    
    if s == None or s=='':
        msg = (f'no syllabus body found: {course}')
        
    else: 
        soup = BeautifulSoup(s, 'html.parser')
        
        # find anything of class=instructure_file_link
        links = soup.findAll("a", class_="instructure_file_link")
        n_links = len(links)
        
        # if no links, then no links found
        if n_links == 0:
            msg = (f'no syllabus links found: {course}')
        
        else:

            msgs = []
            successes = 0 
            for c, l in enumerate(links, 1):
                file_name = f'{year}-{name}-{c}'
                msg_l, success = _download_file(l, canvas, file_name,auth_header)
                if success == 1:
                    msgs.append(msg_l)
                successes += success
                
            msg = f'found {n_links} links and {successes} syllabi in {course}'
            msg = f'{msg}: {msgs}'

    return(msg)
    
def _create_api_download(href):

    match_ex = re.compile('(.*)/courses/([0-9]*)/files/([0-9]*)')
    match_response = re.match(match_ex, href)
    if match_response:
        url = match_response[1]
        course_id = match_response[2]
        file_id = match_response[3]

        file_api_url = f'{url}/api/v1/courses/{course_id}/files/{file_id}'
        return(file_api_url)

def _download_file(link, canvas, file_name, auth_header): 

    #first try endpoint
    # # if that doesn't work, use old method   
    file_endpoint = link.get('data-api-endpoint')
    msg = ''
    success = 0

    if file_endpoint == None:
        msg = f'no data-api-endpoint found, tried to create one'
        print(msg)
        #try to get using href
        href = link.get('href')
        file_endpoint = _create_api_download(href)
    
    try:
        file = requests.get(file_endpoint, headers=auth_header)
        file_info = file.json()
        if file_info==None:
            msg = f'no file info found'
            print(msg)
        
        else:
            try:
                file_id = file_info['id']
                #id ,mime_class, content-type, url, display_name
                file_type = file_info['mime_class']
                file_save = f'pdf/{file_name}.{file_type}'

                # check to see if pdf/ directory already exists, if not, makes one
                if not os.path.isdir('pdf'):
                    os.mkdir('pdf')

                # download the canvas file (specified by id) to location: pdf/...
                canvas.get_file(file_id).download(file_save)
                msg = f'{file_save}'
                success = 1

            except Exception as e:
                msg = f'error in file download: {e}'

    except Exception as e:
        cprint(f'Error getting file info\n{e}\n...', 'red')
    
    return(msg, success)