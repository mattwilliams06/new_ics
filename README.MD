# EDO School Shipbuilding ICS Simulator

This repository contains all necessary files to deploy the ICS simulator on Heroku. All necessary dependencies are contained in both the environment.yml and requirements.txt files. The author created the simulator in an Anaconda environment using Python 3.7. 

ics_main.py is the main script containing the simulator. The script uses the Streamlit library for web app integration. No HTML or CSS is required to deploy. There are very few parameters one would ever need to adjust within ics_main.py, but each will be lited below.

## User passwords
These can be found in the _main()_ function within ics_main.py, stored as a list in the variable _passwords._