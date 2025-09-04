import json
from xml.etree.ElementTree import indent

# reading djson datset
with open("data.json", 'r') as file:
    read_data = json.load(file)
    print(read_data)