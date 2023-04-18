## Start greengrass:

cd /greengrass/ggc/core/
sudo ./greengrassd start

## Publisher and subscriber demo (part 1):
Publisher : 96bcbf21eba7341d3c0f94c8bfc136c2fbbad26f6be3a601302d91e361487f0b
Subscriber: d023941f6eacd552ae3821c32a2e0df2d6b16ddc399738ac31059d455a7967e4
Greengrass cert id: 
e04b1ff5b373c2ff04fb4e50203e5e053c421aa0de22da22e7a659a8bbd5fdbd

aws iot endpoint: a1cz6eeuu9fdle-ats.iot.us-west-2.amazonaws.com

cd publisher_certs
python basicDiscovery.py --endpoint a1cz6eeuu9fdle-ats.iot.us-west-2.amazonaws.com --rootCA AmazonRootCA1.pem --cert 96bcbf21eba7341d3c0f94c8bfc136c2fbbad26f6be3a601302d91e361487f0b-certificate.pem.crt --key 96bcbf21eba7341d3c0f94c8bfc136c2fbbad26f6be3a601302d91e361487f0b-private.pem.key --thingName HelloWorld_Publisher --topic 'hello/world/pubsub' --mode publish --message 'Hello, World! Sent from HelloWorld_Publisher'

cd subscriber_certs
python basicDiscovery.py --endpoint a1cz6eeuu9fdle-ats.iot.us-west-2.amazonaws.com --rootCA AmazonRootCA1.pem --cert d023941f6eacd552ae3821c32a2e0df2d6b16ddc399738ac31059d455a7967e4-certificate.pem.crt --key d023941f6eacd552ae3821c32a2e0df2d6b16ddc399738ac31059d455a7967e4-private.pem.key --thingName HelloWorld_Subscriber --topic 'hello/world/pubsub' --mode subscribe


###### Part 2 running

Sending Data:
python basicDiscovery.py --endpoint a1cz6eeuu9fdle-ats.iot.us-west-2.amazonaws.com --rootCA AmazonRootCA1.pem --cert "certificates/0/cert.pem" --key "certificates/0/private.key" --thingName 0 --topic 'iot/car2core/0' --mode publish --data "data2/vehicle0.csv"

Receiving data:
python basicDiscovery.py --endpoint a1cz6eeuu9fdle-ats.iot.us-west-2.amazonaws.com --rootCA AmazonRootCA1.pem --cert "certificates/0/cert.pem" --key "certificates/0/private.key" --thingName 0 --topic 'iot/core2car/0' --mode subscribe --data "data2/vehicle0.csv"

Do this for 4 other cars ...


