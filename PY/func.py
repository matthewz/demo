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
                      , default="ALL"
                      , nargs="?"
                      , help="app = ALL(default) , app, abc, tla, fcb, googl, ibm, aol, any, all"
                      )
   parser.add_argument("--env"
                      , default="ALL"
                      , nargs="?"
                      , help="env = ALL(default), qal, pte, stg, prd, ALL"
                      )
   parser.add_argument("--type"
                      , default="java"
                      , nargs="?"
                      , help="type = rpm(default), tomcat, zip, java"
                      )
   parser.add_argument("--action"
                      , default="info"
                      , nargs="?"
                      , help="action = info(default), build, package, ship, install, deploy, verify, compute"
                      )
   parser.add_argument("--file"
                      , default=""
                      , nargs="?"
                      , help="file = full path to file containing further arguments or data"
                      )
   parser.add_argument("--proj"
                      , default="ALL"
                      , nargs="?"
                      , help="proj = ALL(default), [GCP Project Name]...e.g. " + args.app_project_prefix + "${ENV}"
                      )
   parser.add_argument("--shared_project"
                      , default=args.dns_project_prefix 
                      , nargs="?"
                      , help="shared_project = " + args.dns_project_prefix + "${env}(default), [GCP Project Name containing DNS Zone]"
                      )
   parser.add_argument("--images_project"
                      , default=args.img_project 
                      , nargs="?"
                      , help="images_project = team-images-project(default), [GCP Project Name containing base images]"
                      )
   parser.add_argument("--zone"
                      , default="ALL"
                      , nargs="?"
                      , help="zone = ALL(default) GCE zone to list / modify...e.g. us-west2-a"
                      )
   parser.add_argument("--dns_zone"
                      , default=args.dns_zone_suffix
                      , nargs="?"
                      , help="dns_zone = internal.zone where DNS Records are stored...e.g. ${ENV}" +  args.dns_zone_suffix 
                      )
   parser.add_argument("--region"
                      , default="ALL"
                      , nargs="?"
                      , help="region = ALL(default) GCE zone to list / modify...e.g. us-east1"
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
   if args.cmd_line_args.shared_project == args.dns_project_prefix:
      args.cmd_line_args.shared_project = args.dns_project_prefix + args.cmd_line_args.env
   if args.cmd_line_args.dns_zone == args.dns_zone_suffix:
      args.cmd_line_args.dns_zone = args.cmd_line_args.env + args.cmd_line_args.dns_zone
   if args.cmd_line_args.app == "ALL":
      args.app_filter = "*"
   else: 
      args.app_filter = args.cmd_line_args.app + "*"
   return True 
# TODO: scan DNS for both shared-$ENV and shared-ext-$ENV, set all env as global variables here, and, handle nonprod vs. prod as well as the six, dev, qal, pte, stg, prd, and, what about app filter(does not work for images et al)> , do we need some more arguments...26 maybe?, add gcloud cmd as an arguement to --action, maybe make --action a list of selections...if not already , why does from module import module blah blah have to be done?, ensure all arg defaults are correct and synch. with constances in pvars.py 
