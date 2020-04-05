# EDO School Shipbuilding ICS Simulator

This repository contains all necessary files to deploy the ICS simulator on Heroku. All necessary dependencies are contained in both the environment.yml and requirements.txt files. The author created the simulator in an Anaconda environment using Python 3.7. 

ics_main.py is the main script containing the simulator. The script uses the Streamlit library for web app integration. No HTML or CSS is required to deploy. There are very few parameters one would ever need to adjust within ics_main.py, but each will be lited below.

## User passwords
These can be found in the _main()_ function within ics_main.py, stored as a list in the variable _passwords._ The passwords are used to assign the number of tests to be performed. This is done in the _perform_calcs()_ function, as a dictionary stored in the _test_dict_ variable. The names of the passwords and the number of tests can easily be changed. Remember to change the password names in both locations.

The administrator password bypasses the built-in wait time that the other passwords have.

## CDD parameters
These are found in _perform_calcs()_ and are the threshold values taken from the CDD

## Normal distribution parameters
Each parameter for each test is computed by taking the threshold values and multiplying by a factor that was taken from one of three normal distributions. There are three options for each configuration item that the user can select. The option selected determines which factor is used. Those factors are created in _perform_calcs()_ and are p1, p2, and p3. The function _np.random.normal_ returns a sample from a normal distribution. The first argument is the mean, and the second argument is the standard deviation. The means may be changed (currently 0.95, 1.0, and 1.05). The means stay the same for each test, but the standard deviations are changed by sampling a uniform distribution. Those are stored in _p1_std_, _p2_std_, and _p3_std_.

Each individual CDD parameter gets three factors each test. The factor corresponding to the user choice is selected using a dictionary. For example, if the user selected an engine size of _medium_, then the second factor, _p2_, would be used (_p1_ is for small and _p3_ is for large, etc for each user choice). The factor is multiplied by the CDD parameter to determine the value for that test. The speed has an additional factor to account for selecting a more streamlined hull form.

## Time per test
This can be adjusted by changing _test_len_, which is set in the _progress_bar()_ function. The first part of the _if_ statement is for the administrator password, and that should be left ar 1 second for testing purposes. The second part sets the time for all other passwords. The _test_len_ parameter is in seconds. 

Note that as the user orders more tests, a learning curve is achieved, and every 5 tests the total time to conduct the next 5 batches of tests is reduced by _test_len_. That is, let's say the _test_len_ parameter is currently set to 120 seconds (2 minutes). If the user orders 15 tests, the test time parameter computes the total time to run all 15 tests as 1440 seconds (24 minutes). Note that this is less than 30 minutes. Each batch of 5 tests reduces the time by 2 minutes. Therefore, 3 batches of 5 tests reduces the total time by 3 * 2 - 6 minutes.