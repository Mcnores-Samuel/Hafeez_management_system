#!/usr/bin/env python3

from uuid import uuid4
import json
import time


def generate_and_store_special_code():
    while True:
        print("Generating the code....")
        with open('cryptic_core_app/protected_codes/agent_code.json', "w") as file:
            json.dump(str(uuid4()), file, indent=4)
        time.sleep(5 * 60)