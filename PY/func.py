
###############################################################
#   Please see: https://developers.google.com/apis-explorer   #
###############################################################

def list_instances(compute, project, zone):
   request = compute.instances().list(project=project, zone=zone)
   response = request.execute()
   if "items" in response:
      return response["items"] 
   else:
      #return ERROR?
      pass

def list_addresses(compute, project, region):
   request = compute.addresses().list(project=project, region=region)
   response = request.execute()
   if "items" in response:
      return response["items"] 
   else:
      #return ERROR?
      pass

def list_forwarding_rules(compute, project, region):
   request = compute.forwardingRules().list(project=project, region=region)
   response = request.execute()
   if "items" in response:
      return response["items"] 
   else:
      #return ERROR?
      pass

def list_record_sets(dns, project, zone):
   request = dns.resourceRecordSets().list(project=project, managedZone=zone)
   response = request.execute()
   if "rrsets" in response:
      return response["rrsets"] 
   else:
      #return ERROR?
      pass

def list_images(compute, project):
   request = compute.images().list(project=project)
   response = request.execute()
   if "items" in response:
      return response["items"]
   else:
      #return ERROR?
      pass
