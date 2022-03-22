
###############################################################
#   Please see: https://developers.google.com/apis-explorer   #
###############################################################

import pvars as args

def list_regions(compute, project):
   request = compute.regions().list(project=project)
   response = request.execute()
   if "items" in response:
      return response["items"] 
   else:
      #return ERROR?
      pass

def list_zones(compute, project):
   request = compute.zones().list(project=project)
   response = request.execute()
   if "items" in response:
      return response["items"] 
   else:
      #return ERROR?
      pass

def get_disk(compute, project, zone, disk):
   request = compute.disks().get(project=project, zone=zone, disk=disk)
   response = request.execute()
   if response:
      return response
   else:
      #return ERROR?
      pass

def list_instances(compute, project, zone):
   filter = "name:" + args.app_filter
   request = compute.instances().list(project=project, zone=zone, filter=filter)
   response = request.execute()
   if "items" in response:
      return response["items"] 
   else:
      #return ERROR?
      pass

def list_addresses(compute, project, region):
   filter = "name:" + args.app_filter
   request = compute.addresses().list(project=project, region=region, filter=filter)
   response = request.execute()
   if "items" in response:
      return response["items"] 
   else:
      #return ERROR?
      pass

def list_forwarding_rules(compute, project, region):
   filter = "name:" + args.app_filter
   request = compute.forwardingRules().list(project=project, region=region, filter=filter)
   response = request.execute()
   if "items" in response:
      return response["items"] 
   else:
      #return ERROR?
      pass

def list_record_sets(dns, project, zone):
   #filter = "name:" + args.app_filter
   #request = dns.resourceRecordSets().list(project=project, managedZone=zone, filter=filter)
   request = dns.resourceRecordSets().list(project=project, managedZone=zone)
   response = request.execute()
   if "rrsets" in response:
      return response["rrsets"] 
   else:
      #return ERROR?
      pass

def list_images(compute, project):
   #ALERT!: this is a hack to make it work for p4 only
   if args.cmd_line_args.app == "p4":
   #TODO: multiple and/or filters - how to?
      #filter = "family:" + args.img_filter_family + " , " + "name:" + args.img_filter_prefix_1 + "*"
      filter = "name:" + args.img_filter_prefix_1 + "*"
   else:
      filter = "name:" + args.img_filter_prefix_2 + args.cmd_line_args.app + "*"
#
   #filter = "name:" + args.img_filter_prefix_2 + args.cmd_line_args.app + "*"
#
   request = compute.images().list(project=project, filter=filter)
   response = request.execute()
   if "items" in response:
      return response["items"]
   else:
      #return ERROR?
      pass
# TODO: do valid ERROR? return code checking and handling...logical and processing errors, catch/try/otherwise stuff. 
