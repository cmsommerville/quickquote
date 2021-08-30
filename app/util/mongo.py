from pymongo.cursor import Cursor


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
