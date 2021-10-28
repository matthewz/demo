#!/usr/bin/env python3
 
import pvars as args
#import init
from init import *
#import func
from func import *

def initialization(): 
   args.init()
   args.cmd_line_args = parse_args()
   RC = validate_args()
   if RC:
      pass
   else:
      print("Invalid command line args, exiting...")
      return False
   log_level_nbr = getattr(logging, args.cmd_line_args.log_level.upper(), "UNDEFINED")
   logging.basicConfig(level=log_level_nbr
                      , filename=args.cmd_line_args.log_path
                      , format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"
                      ) 
   logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
   logging.info("*****************************************************")
   logging.info(f"  My Fancy Multi-utility / Version: {args.version}  ")
   logging.info("*****************************************************")
   return True

def extract_data():
   logging.info("Entering extract_data...")
   if args.cmd_line_args.action in ["info"]:
      compute = googleapiclient.discovery.build("compute", "v1")
      dns = googleapiclient.discovery.build("dns", "v1")
      project = args.cmd_line_args.proj
      shared_project = args.cmd_line_args.shared_project
      images_project = args.cmd_line_args.images_project
      region = args.cmd_line_args.region
      zone = args.cmd_line_args.zone
      dns_zone = args.cmd_line_args.dns_zone
      instances = list_instances(compute, project, zone)
      addresses = list_addresses(compute, project, region)
      forwarding_rules = list_forwarding_rules(compute, project, region)
      record_sets = list_record_sets(dns, shared_project, dns_zone)
      images = list_images(compute, images_project)

      print("Instances in project %s and zone %s:" % (project, zone))
      for item in instances:
         print("Instance - " + item["zone"] + " | " + item["name"] + " | " + item["networkInterfaces"][0]["networkIP"])

      print("Load Balancers in project %s and region %s:" % (project, region))
      for item in addresses:
         print("Load Balancer - " + item["region"] + " | " + item["name"] + " | " + item["address"])

      print("Internal DNS's in project %s and region %s:" % (project, region))
      for item in forwarding_rules:
         service_name = item.get("serviceName")
         if service_name:
            print("Service - " + item["name"] + " | " + service_name)
         else:
            print("Service - " + item["name"] + " | " + "None")

      print("Primary DNS records in shared project %s and DNS Zone %s:" % (shared_project, dns_zone))
      for item in record_sets:
         ttl = str(item["ttl"])
         rrdatas = item["rrdatas"]
         for rrdata in rrdatas:
            print("DNS Record - " + item["name"] + " | " + item["type"] + " | " + ttl + " | " + rrdata)

      print("Images in project %s:" % (project))
      for item in images:
         family = item.get("family")
         if family:
            print("Image - " + item["name"] + " | " + family + " | " + item["status"])
         else:
            print("Image - " + item["name"] + " | " + "None" + " | " + item["status"])

def do_smt_else():
   logging.info("Do something else here, then")
 
def processing():
   if args.cmd_line_args.action in ["info", "build", "package", "ship", "install", "deploy", "verify"]:
      extract_data()
   else:
      do_smt_else()

def termination(RC):
   if RC:
      logging.info("exiting...NORMAL")
   else:
      logging.error("exiting...ERROR")

if __name__ == "__main__":
   RC = initialization()
   if RC:
      processing()
   else:
      pass
   termination(RC)
