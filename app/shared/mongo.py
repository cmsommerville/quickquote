from pymongo.cursor import Cursor
import uuid


def projectMongoResults(data, keys=None):
    result = []
    if type(data) == Cursor:
        for row in data:
            d = formatMongoID({k: v for k, v in row.items()})
            if keys:
                result.append({k: v for k, v in d.items() if k in keys})
            else:
                result.append({k: v for k, v in d.items()})
        return result
    else:
        return [formatMongoID({k: v for k, v in data.items()})]


def formatMongoID(d):
    return {k: str(v) if k == "_id" else v for k, v in d.items()}


def generateUUID(arr):
    l = []
    isDict = False
    if type(arr) not in [list, dict]:
        raise Exception("Please pass a dictionary or list")

    if type(arr) == dict:
        isDict = True
        arr = [arr]

    for obj in arr:
        newObj = {}
        if type(obj) != dict:
            continue

        for k, v in obj.items():
            if type(v) in [dict, list]:
                try:
                    v = generateUUID(v)
                except:
                    print(v)
                    raise
            newObj = {**newObj, k: v}

        l.append({"uuid": str(uuid.uuid4()), **newObj})

    if isDict:
        return l[0]
    return l
