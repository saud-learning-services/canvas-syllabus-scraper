<p align="center">
<img src="https://physicaltherapy.med.ubc.ca/files/2012/05/UBC-logo-signature-blue.gif" height=15% width=15%
</p>
  
# Syllabus scraper

#### DO NOT DELETE pdf folder

The scraper goes through a subaccount (or a CSV called course_IDs.csv) and looks through each course's 'Syllabus' tab and downloads all .pdf files present and renames each of them according to course code and year (into the pdf folder).

dl_data.csv tells you what files were downloaded for each course.

## Instructions:
1. If you do not have Python, install it. If you have no experience with it, I recommend installing it through *https://www.anaconda.com/download/*.

2. Clone this GitHub repository.

3. Install all the dependencies using pip (first time use only). Use the command **pip install -r requirements.txt** through the command shell in the directory of your cloned GitHub repo.

4. Run the script. It will prompt you for your these things:
   1. Token (Canvas API token)
   2. Subaccount to run in
   3. Term to search through

**Please note this script is rather slow. Due to the risk of taking down the AWS server, all API calls are done on a single thread.**
**This script will be rewritten soon.**
