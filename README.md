# scheduler
A simple app that asks what you are doing. Estimates how long that task should take using the lower bound of a 95% confidence interval, and then will ask you again after that time has elapsed to build up a schedule. It also had an invalde time peroid which will log in nonactivity.


THIS IS SUPER MESSY SO PLEASE IGNORE HOW BAD THE CODE IS

## Features
* Infinite loop that runs the scheduler
* Checks if user is currently in an activity or not
* Inputs non-activity during invalid times
* A small program to load in settings
* Log files to keep a record of activity and to estimate future lengths of activities
