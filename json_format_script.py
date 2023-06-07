#importing libraries
import json
import os

#creating path
path = input("Enter the path to you JSON: ")

# %% [code] {"jupyter":{"outputs_hidden":false},"execution":{"iopub.status.busy":"2023-06-07T12:32:26.578441Z","iopub.execute_input":"2023-06-07T12:32:26.579205Z","iopub.status.idle":"2023-06-07T12:32:26.607021Z","shell.execute_reply.started":"2023-06-07T12:32:26.579165Z","shell.execute_reply":"2023-06-07T12:32:26.605953Z"}}
#storing filename
filename = path .split('\\')[-1]

#storing filetype
if "png" in filename:
    image_type = "image"

#loading the data
with open(path) as f:
    data = json.load(f)



#extracting info from the json

#intializing necessary dictionary and lists
new_name={}
bbox=[]
bbox_vehicle=[]
bbox_license=[]
occlusion=[]

#grabbing info from the JSON
for obj in data['objects']:
    for attr in obj['tags']:
        new_name[attr['name']] = attr['value']
    for x in (obj['points']['interior']):
        occlusion.append(x)
    for x in (obj['points']['exterior']):
        bbox.append(x)
if len(bbox) != 0:
    new_name['bbox_vehicle'] = bbox[0] + bbox[1]
    
    if len(bbox[0] + bbox[1])>0:
        new_name['presence_v'] = 1
    else :
        new_name['presence_v'] = 0
    
    if len(bbox) > 2:
        new_name['bbox_license'] = bbox[2] + bbox[3]
        
        if len(bbox[2] + bbox[3])>0:
            new_name['presence_l'] = 1
        else :
            new_name['presence_l'] = 0
        
new_name['Occlusion'] = len(occlusion)

#checking extracting info
new_name


#tackling missing attributes or objects
list_attr = ["Type","Pose","Model","Make","Color","Difficulty Score","Value","Occlusion"]
list_attr_pr = ["presence_v","presence_l"]
list_attr_bb = ["bbox_vehicle","bbox_license"]

for x in list_attr:
    if x not in new_name:
        new_name[x]=None

for x in list_attr_pr:
    if x not in new_name:
        new_name[x]=0

for x in list_attr_bb:
    if x not in new_name:
        new_name[x]=[]
    

#creating formatted json

formatted_json={}


formatted_json["dataset_name"] = filename
formatted_json["image_link"] = ""
formatted_json["annotation_type"] = image_type
formatted_json["annotation_objects"] = {"vehicle":{"presence": new_name["presence_v"],
                                                  "bbox": new_name["bbox_vehicle"]},
                                     "license_plate":{
                                         "presence": new_name["presence_l"],
                                         "bbox": new_name["bbox_license"]}}
formatted_json["annotation_attributes"] = {"vehicle":{
                                                      "Type":new_name["Type"],
                                                      "Pose": new_name["Pose"],
                                                      "Model": new_name["Model"],
                                                      "Make": new_name["Make"],
                                                      "Color":new_name["Color"]
                                                       },
                                           "license_plate":{
                                               "Difficulty Score":new_name["Difficulty Score"],
                                               "Value":new_name["Value"],
                                               "Occlusion":new_name["Occlusion"]
                                           }}

formatted_json = [formatted_json]

s = json.dumps(formatted_json,indent=4)

print(s)


with open("formatted_"+ filename,"w") as d:
    d.write(s)