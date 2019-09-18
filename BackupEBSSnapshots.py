from datetime import datetime

#Snapshot of EBS Volumes on all regions with a tag name key backup:true

import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
        for region in ec2_client.describe_regions()['Regions']]
        
    for region in regions:
        print('Instances in EC2 region {0}'.format(region))
        ec2 = boto3.resource('ec2', region_name=region)
        
        instances = ec2.instances.filter(
            Filters=[
                {'Name': 'tag:backup', 'Values': ['true']}
            ]
        )
        
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
        
        for i in instances.all():
            for v in i.volumes.all():
                desc = 'Backup of {0}, volume {1}, created {2}'.format(i.id, v.id, timestamp)
                print(desc)
                
                snapshot = v.create_snapshot(Description=desc)
                
                print("Created Snapshot:", snapshot.id)