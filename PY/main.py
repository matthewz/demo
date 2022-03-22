#!/usr/bin/env python3
 
import pvars as args
#import init
from init import *
#import func
from func import *

def init_logging():
   log_level_nbr = getattr(logging, args.cmd_line_args.log_level.upper(), "UNDEFINED")
   logging.basicConfig(level=log_level_nbr
                      , filename=args.cmd_line_args.log_path
                      , format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"
                      )
   logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
   logging.info("*****************************************************")
   logging.info(f"  Multi-utility / Version: {args.version}           ")
   logging.info(f"  Extracts from compute and dns:                    ")
   logging.info(f"  DNS Record, LB Address, FWD Rule, 1nstance, Image ")
   logging.info("*****************************************************")

def initialization(): 
   args.init()
   args.cmd_line_args = parse_args()
   RC = validate_args()
   if RC:
      pass
   else:
      print("Invalid command line args, exiting...")
      return False
   args.compute_api = googleapiclient.discovery.build("compute", "v1")
   args.dns_api = googleapiclient.discovery.build("dns", "v1")
   args.app_envs = []
   if args.cmd_line_args.env == "ALL":
      args.app_envs = ["dev", "qal", "pte", "stg", "prd"]
   else:
      args.app_envs.append(args.cmd_line_args.env)
   init_logging()
   return True

def print_instance_data(project, zone, instance):
   if "disks" in instance:
      disks = instance["disks"]
   for disk_item in disks:
      if disk_item.get("boot"):
         instance_name =  instance["name"]
         disk_name = disk_item.get("source").split("/")[10]
         disk = get_disk(args.compute_api, project, zone, disk_name)
         source_image = disk.get("sourceImage")
         if source_image:
            source_image = source_image.split("/")[9]
         else:
            source_image = "None"
         if instance_name != disk_name:
            disk_name =  disk_name + "(" + "differs" + ")" 
         else:
            disk_name = "same as instance name"
         print("Instance" + " | " + project + " | " + zone + " | " + instance_name + " | " + instance["networkInterfaces"][0]["networkIP"] + " | " + disk_name + " | " +  source_image)
      else:
         pass

def extract_compute_data(zone, project):
   #logging.info("Entering extract_compute...")

   if zone == "ALL":
      zones = list_zones(args.compute_api, project)
      for zone in zones:
         zone = zone["name"]
         instances = list_instances(args.compute_api, project, zone)
         if instances:
            #print("Instances in project %s and zone %s:" % (project, zone))
            for instance in instances:
               print_instance_data(project, zone, instance)
   else:
      instances = list_instances(args.compute_api, project, zone)
      if instances:
         #print("Instances in project %s and zone %s:" % (project, zone))
         for instance in instances:
            print_instance_data(project, zone, instance)

def extract_addresses_and_rules_data(project, region):
   addresses = list_addresses(args.compute_api, project, region)
   if addresses:
      #print("Load Balancers in project %s and region %s:" % (project, region))
      for address in addresses:
         print("LB Address" + " | " + project + " | " + region + " | " + address["name"] + " | " + address["address"])
   forwarding_rules = list_forwarding_rules(args.compute_api, project, region)
   if forwarding_rules:
      #print("Internal DNS's in project %s and region %s:" % (project, region))
      for rule in forwarding_rules:
         service_name = rule.get("serviceName")
         if not service_name:
            service_name = "None"
         print("Forwarding Rule" + " | " + project + " | " + region + " | " + rule["name"] + " | " + service_name)

def extract_instance_data(project):
   #logging.info("Entering extract_data...")
   region = args.cmd_line_args.region
   zone = args.cmd_line_args.zone

   if args.cmd_line_args.action in ["compute"]:
      pass 
   else:
      if region == "ALL":
         regions = list_regions(args.compute_api, project)
         for region in regions:
            region = region["name"]
            extract_addresses_and_rules_data(project, region)
      else:
         extract_addresses_and_rules_data(project, region)
   extract_compute_data(zone, project)

def extract_dns_data(project, zone):
   record_sets = list_record_sets(args.dns_api, project, zone)
   for resource in record_sets:
      ttl = str(resource["ttl"])
      rrdatas = resource["rrdatas"]
      for rrdata in rrdatas:
         #if args.app_filter in resource["name"]:
         if args.cmd_line_args.app in resource["name"]:
            print("DNS Record" + " | " + project + " | " + resource["name"] + " | " + resource["type"] + " | " + ttl + " | " + rrdata)

def extract_images_data(project):
   images = list_images(args.compute_api, project)
   if images:
      for image in images:
         family = image.get("family")
         if not family:
            family = "None"
         print("Image" + " | " + project + " | " + image["name"] + " | " + family + " | " + image["status"])

def do_smt_else():
   logging.info("Do something else here, then...")

def process_all_project_app_envs(project):
   if project == "ALL":
      for env in args.app_envs:
         extract_instance_data(args.app_project_prefix + env)
   else:
      extract_instance_data(project) 

def do_something():
   if args.cmd_line_args.action in ["info"]:
      for env in args.app_envs:
         dns_project = args.dns_project_prefix + env
         zone = env + args.dns_zone_suffix
         extract_dns_data(dns_project, zone)
      process_all_project_app_envs(args.cmd_line_args.proj)
      extract_images_data(args.cmd_line_args.images_project)
   elif args.cmd_line_args.action in ["compute"]:
      process_all_project_app_envs(args.cmd_line_args.proj)
   else:
      pass
 
def processing():
   if args.cmd_line_args.action in ["info", "build", "package", "ship", "install", "deploy", "verify", "compute"]:
      do_something()
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
# TODO: refactor prococessing function into do something and do something else based on action(s), all functions should be 20 lines or less and limit use a global if possible..., same as in other modules, why the import module as...? blah blah. 
