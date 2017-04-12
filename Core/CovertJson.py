import shelve
import json

def covert_json(shelve_file_name):
    shv = shelve.open(shelve_file_name)
    d = dict()
    for key, val in shv.iteritems():
        d[key] = str(val)
    shv.close()
    return json.dumps(d).encode('utf-8')