import json
import os, sys, traceback
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


# create a MongoClient instance
client = MongoClient("localhost", 27017)
db = client.members
posts = db.member_info

# configure the path to files
path = "/data/path"
files = os.listdir(path)
files.sort()

counter = 0

for jsonf in files:
    nullId = list()
    flag = False

    try:
        wholePath = [path, jsonf]
        with open("/".join(wholePath), "r") as f:
            members = json.load(f)
    except Exception as e:
        print("[ERROR] Encounter {0} while processing \"{2}\": {1}".format(type(e), e, jsonf))
        traceback.print_exc()
        continue

    try:
        for (key, value) in members.iteritems():
            if value is None:
                flag = True
                nullId.append(key)
            else:
                value["_id"] = key
                try:
                    posts.insert_one(value)
                except DuplicateKeyError:
                    pass
    except Exception as e:
        print("[ERROR] {0}: {1}".format(type(e), e))
        traceback.print_exc()
        pass
    
    if flag:
        with open("./need_further_process.txt", "a") as f:
            f.write(str(nullId))
            f.write("\n")
            f.flush()    
    counter += 1
    print(str(datetime.now()) + ": {},000 members({}) have been processed.\n".format(counter, jsonf))
    del members
    del nullId
