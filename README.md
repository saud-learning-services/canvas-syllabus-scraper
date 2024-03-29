# Canvas Syllabus Scraper

> - name: canvas-syllabus-scraper
> - run-with: terminal
> - python>=3.7
> - canvasapi>=2.0.0
> - custom environment: canvas-syllabus-scraper

## Summary

This project takes an account id as input and attempts to download any syllabi for courses in that account. The user can specify

1. The term or year to filter to (uses "startswith" regex to match). For example, 2020 would include 2020W1-2, 2020W1, 2020W2, 2020S etc.
2. Terminal will ask for inputs and confirmations
3. Errors will be shown when necessary by the interface (also shows skipped courses that do not match term)
4. A file with the entered term or year will be generated to show the status of each attempted course file
5. Final files can be found in the folder pdf/

## :warning: Important Caveats

- This script is slow! It makes at least one request per course (depending on number of links found)
- We recommend running this script for specific terms or years (not all courses in accounts)
- The script is set to run in the PROD environment of canvas (url = "https://ubc.instructure.com/")
  > _this is set as url in the functon `get_user_inputs()` in the file src/helpers.py_

### Inputs Required

1. Canvas API Token
1. Canvas Account ID
1. Canvas Term or Year required

## To Run

You will need to create the canvas-syllabus-scraper environment. We use [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) to manage our projects. Part of Learning Services and need any other help? Checkout our [docs](https://github.com/saud-learning-services/instructions-and-other-templates)!

### First Time
1. Clone **canvas-syllabus-scraper** repository
1. Install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) (Python 3.7 version)
1. Import environment: `$ conda env create -f environment.yml`

### Every Time (Terminal)
1. Run
   1. `$ conda activate canvas-syllabus-scraper`
   2. `$ python src/syllabus_downloader.py`


---

## Acknowledgement :star2:

This adapatation was forked from https://github.com/ubccapico/syllabus-scraper where the original authors are:

> ### Original Authors
> - **Jeremy Hidjaja** - [JeremyH011](https://github.com/JeremyH011)
> - **Barish Golland** - [barishgolland](https://github.com/barishgolland)

### Additional Contributers
- Marko Prodanovic - [markoprodanovic](https://github.com/markoprodanovic)
- Alison Myers - [alisonmyers](https://github.com/alisonmyers)
- Peter Lukasik - [peterlukasik](https://github.com/peterlukasik)
