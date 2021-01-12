# Canvas Syllabus Scraper

This project takes an account id as input and attempts to download any syllabi for courses in that account. The user can specify

1. The term or year to filter to (uses "startswith" regex to match). For example, 2020 would include 2020W1-2, 2020W1, 2020W2, 2020S etc.
2. Terminal will ask for inputs and confirmations
3. Errors will be shown when necessary by the interface (also shows skipped courses that do not match term)
4. A file with the entered term or year will be generated to show the status of each attempted course file
5. Final files can be found in the folder pdf/

## :warning: Important Caveats

- This script is slow! It makes at least one request per course (depending on number of links found)
- We recommend running this script for specific terms or years (not all courses in accounts)
- The script is set to run in the TEST environment of canvas (url = "https://ubc.test.instructure.com/") which is 2 weeks behind the PROD canvas instance but otherwise a mirror
  > _this is set as url in the functon `get_user_inputs()` in the file src/helpers.py_

## To Run

### First Time

You will need to create the canvas_syllabi environment. We use conda to manage our projects.
(This should also work with the sauder_canvas_api environment)
`$ conda env create -f environment.yml`

### Every Time

1. `$ conda activate canvas-syllabus-scraper`
1. `$ python src/syllabus_downloader.py`

### Inputs for Required

1. Canvas API Token
1. Canvas Account ID
1. Canvas Term or years

---

## Acknowledgement :star2:

This adapatation was forked from https://github.com/ubccapico/syllabus-scraper where the original authors are:

> ### Original Authors
>
> - **Jeremy Hidjaja** - [JeremyH011](https://github.com/JeremyH011)
> - **Barish Golland** - [barishgolland](https://github.com/barishgolland)
