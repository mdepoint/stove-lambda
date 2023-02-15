import json
import os

import requests

# from botocore.vendored import requests


def lambda_handler(event, context):

    device_id = os.getenv("DEVICE_ID")
    access_token = os.getenv("access_token")

    nest_url = f"https://developer-api.nest.com/devices/thermostats/{device_id}?auth={access_token}"

    r = requests.get(nest_url)
    if r.status_code != 200:
        print(r.text)
    assert r.status_code == 200
    device = r.json()

    high_temp = 73
    lower_temp = 72

    set_temp = None

    print(
        "state: {}   target temp: {}".format(
            device["hvac_state"], device["target_temperature_f"]
        )
    )

    # If the stove is off and we are at the high set temp,
    # lower set temp to the lower set temp
    if device["hvac_state"] == "off" and device["target_temperature_f"] == high_temp:
        print("Lowering target temperature")
        set_temp = lower_temp

    # If the stove is on, and our set temp is the lower temp
    # raise the target to the higher temp
    if (
        device["hvac_state"] == "heating"
        and device["target_temperature_f"] == lower_temp
    ):
        print("Raising target temperature")
        set_temp = high_temp

    # if we have a new set temp, set it
    if set_temp:
        print("Setting Temp to: {}".format(set_temp))
        r = requests.put(nest_url, json={"target_temperature_f": set_temp})
        assert r.status_code == 200
    else:
        print("Leaving temp at: {}".format(device["target_temperature_f"]))

    return {"statusCode": 200, "body": None}
