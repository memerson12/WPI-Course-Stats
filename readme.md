# WPI Course Rating Statistics

This is just a quick script I used to get some stats about the wpi professors.

Main.py pulls current WPI course catalog and then pulls the course reports for all of those classes and saves it to a
json file.

Statistics.py loads the json file and does some simple statistics with it which are saved in the results folder as CSVs.

If you want to run it yourself, you will need to log into [oscar.wpi.edu]() and copy the MOD_AUTH_CAS_S cookie and put
it in at the top of CourseReports.py.

