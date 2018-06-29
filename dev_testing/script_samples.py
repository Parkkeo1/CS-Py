# standalone helper script, used for testing

import json
import requests

# testing with round_data json file instead of match_data
with open('midround_death_data.json') as json_file:
    data = json.load(json_file)

r = requests.post('http://127.0.0.1:5000/api', json=data)
print(r.status_code)
print(r.headers)
print(r.text)


