#from hats_rest.models import Hat
import django
import os
import sys
import time
import json
import requests

sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hats_project.settings")
django.setup()

# Import models from hats_rest, here.
# from hats_rest.models import Something

from hats_rest.models import BinVO

def poll():
    while True:
        print('Hats poller polling for data')
        try:
            url = "http://wardrobe-api:8000/api/bins/"
            response = requests.get(url)
            content = json.loads(response.content)
            for bin_data in content['bins']:
                BinVO.objects.update_or_create(
                    href = bin["href"],
                    defaults={
                        "closet_name": bin["closet_name"],
                        "bin_number": bin["bin_number"],
                        "bin_size": bin["bin_size"]
                    }
                )


        except Exception as e:
            print(e, file=sys.stderr)
        time.sleep(60)


if __name__ == "__main__":
    poll()


#def get_bin():
    #variable with content
    #variable = result of requests to get info from API endpoint
    #dict = dump/load json (it's either dumping or loading to parse the json, she owuldn't say)
    #for loop over dictionary and look through content in dictionary values
        #this is to be able to get a single desired bin

    #This poller continually polls a bin and when it notices a change
    # in the dictionary being looped over
    # it will push that change into the value object
        # This part hasn't been pseudocoded yet


# Declare a function to update the AccountVO object (ch, method, properties, body)
#   content = load the json in body
#   first_name = content["first_name"]
#   last_name = content["last_name"]
#   email = content["email"]
#   is_active = content["is_active"]
#   updated_string = content["updated"]
#   updated = convert updated_string from ISO string to datetime
#   if is_active:
#       Use the update_or_create method of the AccountVO.objects QuerySet
#           to update or create the AccountVO object
#   otherwise:
#       Delete the AccountVO object with the specified email, if it exists
