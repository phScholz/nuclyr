import os
import json

print("!!!nuclyr config file loaded!!!")

config = {
    "webdriver" :   "Edge",
    "driver_loc":   "",
    "output"    : False,
    "outputDir" : "./output",
    "installDir":   os.path.dirname(__file__)     
}

if not os.path.exists(os.path.join(os.path.expanduser('~'),".nuclyr")):
    json.dump(config, open(os.path.join(os.path.expanduser('~'),".nuclyr"),"w"))

def Get(option):    
    jsonData = json.load(open(os.path.join(os.path.expanduser('~'),".nuclyr"),"r"))
    return jsonData[option]

def Set(option, string):
    jsonData = json.load(open(os.path.join(os.path.expanduser('~'),".nuclyr"),"r"))
    jsonData[option] = string
    json.dump(jsonData, open(os.path.join(os.path.expanduser('~'),".nuclyr"),"w"))
    Show()

def Show():
    print(json.load(open(os.path.join(os.path.expanduser('~'),".nuclyr"),"r")))
    
