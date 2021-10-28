import pvars as args
import argparse  
import sys
import json
import logging
from datetime import datetime
import os
import time
import googleapiclient.discovery

"""
def get_timestamp():
   # current date and time
   now = datetime.now()
   return now.strftime("%Y-%m-%d-%H-%M-%S")
"""

def parse_args():
   parser = argparse.ArgumentParser(description="command line arguments...")
   parser.add_argument("--debug"
                      , action="store_true"
                      , help="debug switch - if --debug is found, diagnostics will be turned on"
                      )
   parser.add_argument("--app"
                      , default="app"
                      , nargs="?"
                      , help="app = app(default), abc, tla, fcb, googl, ibm, aol, any, all"
                      )
   parser.add_argument("--type"
                      , default="java"
                      , nargs="?"
                      , help="type = rpm(default), tomcat, zip, java"
                      )
   parser.add_argument("--action"
                      , default="info"
                      , nargs="?"
                      , help="action = info(default), build, package, ship, install, deploy, verify"
                      )
   parser.add_argument("--file"
                      , default=""
                      , nargs="?"
                      , help="file = full path to file containing further arguments or data"
                      )
   parser.add_argument("--proj"
                      , default="app-default-dev"
                      , nargs="?"
                      , help="proj = app-default-dev(default), [GCP Project Name]"
                      )
   parser.add_argument("--shared_project"
                      , default="org-shared-env"
                      , nargs="?"
                      , help="shared_project = org-shared-env(default), [GCP Project Name containing DNS Zone]"
                      )
   parser.add_argument("--images_project"
                      , default="org-images-project"
                      , nargs="?"
                      , help="images_project = team-images-project(default), [GCP Project Name containing base images]"
                      )
   parser.add_argument("--zone"
                      , default="us-east1-a"
                      , nargs="?"
                      , help="zone = use-east1-a(default) GCE zone to list / modify"
                      )
   parser.add_argument("--dns_zone"
                      , default="internal.zone"
                      , nargs="?"
                      , help="dns_zone = internal.zone where DNS Records are stored"
                      )
   parser.add_argument("--region"
                      , default="us-east1"
                      , nargs="?"
                      , help="region = use-east1(default) GCE zone to list / modify"
                      )   
   parser.add_argument("--acct"
                      , default=""
                      , nargs="?"
                      , help="acct = Account ID to use for authentication"
                      )
   parser.add_argument("--token"
                      , default=""
                      , nargs="?"
                      , help="token = auth token or password to use for authentication"
                      )
   parser.add_argument("--log_path"
                      , default="/tmp/my_fab_log.txt"
                      , nargs="?" 
                      , help="log_path = full path to file where log entries should be written"
                      )
   parser.add_argument("--log_level"
                      , default="INFO"
                      , nargs="?"
                      , help="Log level = INFO(default), ERROR, WARNING, DEBUG"
                      )
   return parser.parse_args()

def validate_args():
   if args.cmd_line_args.debug:
      print("Debugging is ENABLED")
   else:
      print("Debugging NOT enabled")
   log_level_nbr = getattr(logging, args.cmd_line_args.log_level.upper(), "UNDEFINED")
   if isinstance(log_level_nbr, int):
      print("INFO - Setting log level to:" + " " + args.cmd_line_args.log_level + "" + "(" + str(log_level_nbr) + ")")
   else:
      print("ERROR - Cannot set log level to:" + " " + args.cmd_line_args.log_level + "" + "(" + str(log_level_nbr) + ")")
      return False
   return True 
