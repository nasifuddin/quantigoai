import pandas as pd 
import os
import json

paths = []

for dirname, _, filenames in os.walk(input("Enter the folder directory: ")):
    for filename in filenames:
        paths.append(os.path.join(dirname, filename))

combined_json=[]

for x in paths:
    with open(x, 'r') as j:
        combined_json.append(json.load(j))
        
with open('combined.json', 'w') as d:
        json.dump(combined_json, d, indent=4)


for x in combined_json:
    for y in x['objects']:
        y['classTitle'] = y['classTitle'].replace("Vehicle","car")
        y['classTitle'] = y['classTitle'].replace("License Plate","number")
        
    

    with open('combined.json', 'w') as d:
        json.dump(combined_json, d, indent=4)