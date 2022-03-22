import sys

#
def init():
    global version
    global cmd_line_args
    global compute_api
    global dns_api
    global app_filter
    global app_envs
    global app_project_prefix
    global dns_project_prefix
    global dns_zone_suffix
    global img_project 
    global img_filter_prefix_1
    global img_filter_prefix_2
    global img_filter_family
#
    version = "0.1.0"
    cmd_line_args = None
    compute_api = None
    dns_api = None
    app_filter = "name:*"
    app_envs = "[dev, qal, pte]"
    app_project_prefix = "acme-proj-"
    dns_project_prefix = "acme-shared-"
    dns_zone_suffix = "-int-acme-ncr-com"
    img_project = "acme-iaas-os-images"
    img_filter_prefix_1 = "acme-centos7-v"
    img_filter_prefix_2 = "acme-ls-c7-"
    img_filter_family = "acme-centos-7"
# TODO: need more constants here, see init.py, ought to make a lot of assumptions, BUT, be configurable to the organization in which it is being run. 
