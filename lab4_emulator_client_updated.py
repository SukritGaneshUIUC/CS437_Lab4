# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np

# xinyihe4@illinois.edu


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 0
device_end = 100

#Path to the dataset, modify this
data_path = "data2/vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = "./certificates/{}/cert.pem"
key_formatter = "./certificates/{}/private.key"


class MQTTClient:

    reccount = 0

    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("a1cz6eeuu9fdle-ats.iot.us-west-2.amazonaws.com", 8883)
        self.client.configureCredentials("./AmazonRootCA1.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))
        MQTTClient.reccount += 1


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, Payload="payload"):
        #TODO4: fill in this function for your publish
        # self.client.subscribeAsync("carSendingData", 0, ackCallback=self.customSubackCallback)
        
        self.client.publishAsync("carSendingData", Payload, 0, ackCallback=self.customPubackCallback)



print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    client.client.connect()
    clients.append(client)

    if (device_id == 0):
        client.client.subscribeAsync("carSendingData", 0, ackCallback=client.customSubackCallback)

 

while True:
    print("reccount:", MQTTClient.reccount)
    print("send now?")
    x = input()
    if x == "s":
        for i,c in enumerate(clients):
            if (i != 0):
                c.publish(json.dumps({"a": 150, "b": 500}))
        print("reccount:", MQTTClient.reccount)

    elif x == "d":
        for c in clients:
            c.client.disconnect()
        print("All devices disconnected")
        exit()
    else:
        print("wrong key pressed")

    time.sleep(3)
