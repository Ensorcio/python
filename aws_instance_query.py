# AWS Instance Query Against List of Instance Names

# Script to query a list of instance names to check for running instances on AWS.
# Run the setToken powershell script or set a AWS token profile before running this script.
# Export a System report from McAfee Epo in .csv format before running this script.
# Written by: Dan Ngo

import boto3
import botocore
import csv

session = boto3.Session(profile_name='token')
ec2r = session.resource('ec2', region_name='us-west-2', api_version='2016-04-01')
instances = open('Systems.csv')
systems = csv.reader(instances, delimiter=",")
instances_aws = []

# Get list of running instances on AWS based on the profile.
running_instances = ec2r.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

# Grab only the instance IDs off of the report.
# The Systems.csv file may include the instance IDs in all upper case. This just makes all the instance ids lowercase.
# Might not be necessary if Python matches are not case sensitive.
for instance_id in instances:
    instances_aws.append(instance_id[0].lower())

# Grab the owner tags off the instances and then compare the instance id of running instances to the instance ids off of the report.
for running_instance in running_instances:
    owner_tags = [d['Value'] for d in running_instance.tags if d['Key'] == 'Owner']
    owner = '' if not owner_tags else owner_tags[0]
    if running_instance.id in instances_aws:
        print((running_instance.id + ',' + owner))
