# Cite: https://github.com/keivanK1/aws-create-thing-boto3

from urllib import response
import boto3

import json
import os

POLICY = 'My_Iot_Policy'
GROUP = 'cars'
GROUP_ARN = 'arn:aws:iot:us-west-2:262628876145:thinggroup/cars'

# ACCESS KEY: AKIAT2JPGT5YUWVE5KXF
# SECRET ACCESS KEY: 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

# function to create a single thing and attach to the group specified in GROUP
def createThing(name):
    os.mkdir(f'certificates/{name}')

    global thingClient
    response = thingClient.create_thing(
        thingName = name
    )

    thingArn = response['thingArn']

    response = thingClient.create_keys_and_certificate(
        setAsActive = True
    )

    certificateArn = response['certificateArn']
    PublicKey = response['keyPair']['PublicKey']
    PrivateKey = response['keyPair']['PrivateKey']
    certificatePem = response['certificatePem']
                            
    with open(f'certificates/{name}/public.key', 'w') as outfile:
            outfile.write(PublicKey)
    with open(f'certificates/{name}/private.key', 'w') as outfile:
            outfile.write(PrivateKey)
    with open(f'certificates/{name}/cert.pem', 'w') as outfile:
            outfile.write(certificatePem)

    thingClient.attach_policy(
        policyName = POLICY,
        target = certificateArn
    )
    thingClient.attach_thing_principal(
        thingName = name,
        principal = certificateArn
    )
    thingClient.add_thing_to_thing_group(
        thingGroupName = GROUP,
        thingGroupArn = GROUP_ARN,
        thingName = name,
        thingArn = thingArn,
        overrideDynamicGroups= False
    )

thingClient = boto3.client('iot')
# iteratively create 100 devices
for i in range(0, 100, 1):
    createThing(str(i))