import boto3
#Clean EBS Volumes that are not attached to EC2

def lambda_handler(object, context):
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
        for region in ec2_client.describe_regions()['Regions']]
    
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)
        print("Region: ", region)
    
        volumes = ec2.volumes.filter(
            Filters=[{'Name': 'status', 'Values': ['available']}])
        
        for volume in volumes:
            v = ec2.Volume(volume.id)
            print("Deleting EBS Volume:{}, Size: {} GB".format(v.id, v.size))
            v.delete()
            