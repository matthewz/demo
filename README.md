#Misc. Info./Maintenance Utility

Documentation: URL / Web. Ref. 

Instructions: to run, cd to the PY directory and run: main.py -h 
              for examples of command line args to run_tests.txt

##Description:
Python calls to handle common tasks that involve GCP information gathering and maintenance activites 
- gcloud API?
- cloud_info.sh - as a wrapper - maybe

##Requirements:
- Python 3.10
- Log folder(s):
  - /tmp/logs?
  - /tmp
- Sub-folders:
  - ?/
  - ?/

##To Do:
- Add some more MODIFY type of functions - not just list
- Genericize the service, action, parameters in func.py somehow
- Need a more robust validate_args
- Add a comments section for each function
- Update this README.MDS
- Fix import statements in main.py 
- Fix error result(bad/invalid data) returned from API functions
- Fix weird warning about auth when running compute/dns API service
- Add a shell script to run as a wrapper or maybe an 80x24 ASCII menu
- Create better tests - make a lot of assumptions(defaults) about the env and args
