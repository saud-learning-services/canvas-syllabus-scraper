# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:25:00 2018

@author: jeremyh2
"""

print("Loading...\n")

try:
    import requests
except:
    import pip
    pip.main(['install', 'requests'])
    import requests

try:
    import pandas as pd
except:
    import pip
    pip.main(['install', 'pandas'])
    import pandas as pd

try:
    import json
except:
    import pip
    pip.main(['install', 'json'])
    import json

'''
try:
    from pyPdf import PdfFileReader
except:
    import pip
    pip.main(['install', 'pyPdf'])
    from pyPdf import PdfFileReader
'''

#Should all be part of default Python 3 libraries
import re
import csv
import urllib.request
import os
import shutil

#Helper Functions:

# Read token from file
#   returns a token string
def get_token():
    with open('Canvas API Token.txt','r') as f:
        for line in f:
            for word in line.split():
               token = word
    return token

# Get course ids from a file
#   Parameters: file_name -> File name to read from (csv)
#               mode -> mode choice of what to read from
#   returns a list of course ids
def get_course_ids(file_name, mode):
    course_ids = []
    with open(file_name, 'r') as course_id_csv:
        csv_data = csv.reader(course_id_csv)
        
        mode_2 = mode
        for indx, x in enumerate(csv_data):
            if(indx == 0):
                if(mode == 2):
                    for idx, title in enumerate(x):
                        if(title == 'id'):
                            mode_2 = idx
                            break
            else:    
                course_ids.append(x[mode_2])
    return course_ids

# Format course code for file saving
#   Parameters: json object to search through
#   returns: a formatted string
def get_course_code(json):
    course_code = str(json[u'course_code'])
    course_code = course_code.replace(' ', '', 1)
    course_code = course_code.replace(' ', '_')
    course_code = course_code.replace('-', '_')
    course_code = course_code.replace('.', '_')
    #print(course_code)
    return course_code

# Gets class list of a subaccount
def get_class_list(account_no, token_h):
    print("Getting classes of subaccount...\n")
    
    url = "https://ubc.instructure.com/api/v1/accounts/" + account_no + "/courses"
    courseInfo =  requests.get(url,headers= {'Authorization': 'Bearer ' + token_h})
    CI_table = pd.read_json(courseInfo.text)
    
    while courseInfo.links['current']['url'] != courseInfo.links['last']['url']:
        courseInfo =  requests.get(courseInfo.links['next']['url'],
                     headers= {'Authorization': 'Bearer ' + token_h})
        CI_sub_table = pd.read_json(courseInfo.text)
        CI_table= pd.concat([CI_table, CI_sub_table])
    
    CI_table.to_csv ('account.csv')

'''
Main Code starts
'''
def run_search():
    url = "https://ubc.instructure.com/api/v1/courses/"
    file_name = 'course_IDs.csv'
    
    #Gets token by reading file
    token = input("Please enter your access token here: ")
    
    #Asks user for mode
    mode = input("By IDs csv (1) or by subaccount #? (2): ")
    
    #If mode is by subaccount, we need to get the class list and read from proper file
    if mode == '2':
        sub = input("Enter subaccount #: ")

        try:
            get_class_list(sub, token)
        except:
            print("\nERROR: BAD TOKEN!\n")
            return
            
        file_name = 'account.csv'
        mode = 2
    #If mode is by IDs.csv, we can read file
    else:
        mode = 0
    
    if(mode == 2):
        desired_year = input("Enter desired year (e.g. 2017): ")
    else:
        desired_year = 0
    
    #Get the list of course IDs we will be combing through
    course_ids = get_course_ids(file_name, mode)
    
    #Open csv to write records into
    myFile = open('dl_data.csv', 'w+', newline='')
    writer = csv.writer(myFile)
    writer.writerow(['Term', 'Course_name', 'Course_id', '# of assured PDF links in Syllabus', '# of URLs', '# of Successful Downloads', 'Files'])
    
    #Destination and current directory to save files to
    current = os.path.dirname(os.path.abspath(__file__))
    dst = current + "/pdf"
    
    #For every course we will be searching its syllabus body and seeing if we can find any hyperlinks
    no_of_courses = len(course_ids)
    for course_index, course in enumerate(course_ids):
        
        #Current course id, get syllabus body from API call
        course_id = course
        chosen_course = requests.get(url + course_id + '?include[]=syllabus_body&include[]=term',
                                 headers= {'Authorization': 'Bearer ' + token})
        chosen_course_json = json.loads(chosen_course.text)
        
        #Extract required values from json object of course
        course_name = str(chosen_course_json[u'name'])
        syllabus_body = str(chosen_course_json[u'syllabus_body'])
        
        #Get proper name for file
        course_code = get_course_code(chosen_course_json)
        term_json = json.dumps(chosen_course_json[u'term'])
        term_json = json.loads(term_json)
        term = str(term_json[u'name'])
        year = str(term_json[u'name'])[0:4]
        
        if(year != desired_year and mode == 2):
            print(term + " " + course_name + " not in correct year (" + str(round((course_index+1)/no_of_courses*100,2)) + "% of total classes searched)\n")
            continue
        
        #Find all assured PDF links and hyperlinks
        list_here = re.findall(r'(title=\"(.*?).pdf\" href=\"(.*?)\")', syllabus_body)
        url_list = re.findall(r'(href=\"(.*?)\")', syllabus_body)
        
        file_names=[]
        length = len(list_here)
        url_length = len(url_list)
        
        downloads = 0
        #If only assured PDF links, download them and save them
        if length != 0 and length == url_length:
            print("Saving files for " + course_name + "...")
            for index, pdf in enumerate(list_here):
                
                #Strip anything else but the download link
                file_url= re.search(r'(https:\S+)', pdf[0])
                file_url = file_url.group(0)[:-1]
                
                print(file_url)
                
                file_name= pdf[1]
                file_names.append(file_name)
                
                #Save file name
                file_name_saved = year + "-" + course_code + "-" + str(index) + ".pdf"
                
                #Download said file
                try:
                    try:
                        urllib.request.urlretrieve (file_url, file_name_saved)
                    except:
                        file_url = file_url.replace("ubc.instructure.com", "canvas.ubc.ca")
                        file_url = file_url.replace("&amp;", "&")
                        urllib.request.urlretrieve (file_url, file_name_saved)
                        
                    shutil.move(current+"/" + file_name_saved, dst)
                    print("\nSaved " + file_name + " as " + file_name_saved + " into " + dst)
                    downloads += 1
                except:
                    try:
                        os.remove(file_name_saved)
                        print("\nFile " + file_name_saved + " cannot be saved. Already exists.")
                    except:
                        print("\nFile " + file_name_saved + " cannot be saved. Not downloadable or unauthorized.")
                        
            print("\n") 
        else:
            #If no links, that's okay
            if(url_length == 0):
                print("\nNo hyperlinks for " + course_name)
            #If links but unsure if PDF links, attempt to download them
            else:
                print("Attempting to download files for " + course_name + "...")
                for index, pdf in enumerate(url_list):
                    
                    #Strip anything else but the download link
                    #file_url= re.search(r'(https:\S+)', pdf[0])
                    #file_url = file_url.group(0)[:-1]
                    file_url = pdf[1]
                    file_name= pdf[1]
                    file_names.append(file_name)
                    
                    #File name to save as 
                    file_name_saved = year + "-" + course_code + "-" + str(index) + ".pdf"
                    
                    #Attempt to download
                    try:
                        urllib.request.urlretrieve (file_url, file_name_saved)
                        shutil.move(current+"/" + file_name_saved, dst)
                        print("\nSaved " + file_name + " as " + file_name_saved + " into " + dst)
                        downloads += 1
                    except:
                        try:
                            os.remove(file_name_saved)
                            print("\nFile " + file_name_saved + " cannot be saved. Already exists.")
                        except:
                            print("\nFile " + file_name_saved + " cannot be saved. Not downloadable.")
                
                print("\n") 
        
        #Write relevant info into data sheet    
        writer.writerow([term, course_name, course_id, length, url_length, downloads, file_names])
        print(term + " " + course_name + " Completed (" + str(round((course_index+1)/no_of_courses*100,2)) + "% of total classes searched)\n")
    
    #Save and close csv file    
    myFile.close()

if __name__ == "__main__":
    print("Welcome!")

    try:
        run_search()
    except:
        input("\nSomething bad happened. Press any key to exit: ")
        
    input("\nBye-bye!")
