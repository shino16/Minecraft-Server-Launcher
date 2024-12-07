import json
import boto3

region = 'ap-northeast-1'

def lambda_handler(event, context):
    ## get query string
    param = event.get('queryStringParameters')
    target_query = param['target']
    action = param['action']

    if target_query == "debug":
        target = "LauncherTestInstance"
    elif target_query == "be":
        target = "Minecraft Bedrock Server"
    elif target_query == "je":
        target = "Minecraft Java Server"
    else:
        return "target : " + target_query + " is undefined."

    client = boto3.client('ec2', region_name=region)
    response = client.describe_instances()

    instanceId = ""

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance['Tags']:
                if tag.get('Key') and tag['Key'] == 'Name':
                    if tag['Value'] == target:
                        instanceId = instance['InstanceId']

    if action == "state":
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['InstanceId'] == instanceId:
                    return instance['State']['Name']
    elif action == "start":
        client.start_instances(InstanceIds=[instanceId])
    elif action == "stop":
        client.stop_instances(InstanceIds=[instanceId])
    else:
        return "action : " + action + " is undefined."
    # for reservation in responce['Reservations']:
    #    for instance in reservation['Instances']:
    #        all_list.append(instance['InstanceId'])

    return "Success"
