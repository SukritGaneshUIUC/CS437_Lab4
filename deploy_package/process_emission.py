import json
import logging
import sys

import greengrasssdk

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

# Counter
# Global c02_max value ensures that for a specific car, max c02 value will be tracked
# As more pieces of data are fed in, max_c02 value will be updated
co_max = 0
co2_max = 0
def lambda_handler(event, context):
    global co_max
    global co2_max
    #TODO1: Get your data
    timestep_time, vehicle_co, vehicle_co2, vehicle_hc, vehicle_nox, vehicle_num = event['timestep_time'], event['vehicle_CO'], event['vehicle_CO2'], event['vehicle_HC'], event['vehicle_NOx'], event['vehicle_num']

    print("got data from vehicle", vehicle_num, "with co2 value of", vehicle_co2)

    #TODO2: Calculate max CO2 emission
    co_max = max(vehicle_co, co_max)
    co2_max = max(vehicle_co2, co2_max)

    #TODO3: Return the result
    client.publish(
        topic="iot/core2car/" + str(vehicle_num),
        queueFullPolicy="AllOrException",
        payload=json.dumps({"vehicle_num": vehicle_num, "vehicle_CO": vehicle_co, "CO_max": co_max, "vehicle_CO2 ": vehicle_co2, "C02_max": c02_max, "timestep_time": timestep_time}),
    )

    return