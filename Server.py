import boto3
import time

# Configuration
AMI_ID = 'ami-0c55b159cbfafe1f0'  # Amazon Linux 2 AMI (for example)
INSTANCE_TYPE = 't2.micro'  # Free tier eligible
KEY_NAME = 'my-ssh-key'  # Replace with your SSH key name
SECURITY_GROUP_NAME = 'squid-proxy-sg'
REGION = 'us-west-2'  # Replace with your desired region


def create_security_group(ec2_client):
    response = ec2_client.create_security_group(
        Description='Security group for Squid proxy',
        GroupName=SECURITY_GROUP_NAME
    )
    security_group_id = response['GroupId']
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 3128,
                'ToPort': 3128,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
    return security_group_id


def create_instance(ec2_resource, security_group_id):
    instances = ec2_resource.create_instances(
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SecurityGroupIds=[security_group_id],
        MinCount=1,
        MaxCount=1
    )
    instance = instances[0]
    instance.wait_until_running()
    instance.reload()
    return instance


def install_squid(instance):
    commands = [
        'sudo apt update -y',
        'sudo apt install -y squid',
        'sudo systemctl enable squid',
        'sudo systemctl start squid'
    ]
    for command in commands:
        instance.ssm_send_command(DocumentName='AWS-RunShellScript', Parameters={'commands': [command]})
        time.sleep(5)


def main():
    ec2_client = boto3.client('ec2', region_name=REGION)
    ec2_resource = boto3.resource('ec2', region_name=REGION)

    security_group_id = create_security_group(ec2_client)
    instance = create_instance(ec2_resource, security_group_id)

    print(f'Instance {instance.id} created. Waiting for SSH access...')
    time.sleep(60)  # Wait for instance to be fully ready

    install_squid(instance)
    print(f'Squid proxy installed on instance {instance.id}.')

    instance.reload()
    print(f'Connect to your proxy server at {instance.public_dns_name}:3128')


if __name__ == '__main__':
    main()
