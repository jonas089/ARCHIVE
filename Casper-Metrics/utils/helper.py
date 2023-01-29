import datetime
from utils.t1m3st4mps import find_earliest_in_timestamp_cost_set, find_latest_in_timestamp_cost_set

def does_key_exist(dict, key):
    if dict.get(key) is not None:
        return True
    else:
        return False

# returns set of deploy headers, sorted by month
def deploys_by_month(set):
    _deploys_by_month = {}
    most_expensive_deploy = 0
    for deploy in set:
        if int(deploy[1]) > most_expensive_deploy:
            most_expensive_deploy = int(deploy[1])
        t = deploy[0]
        _t = datetime.datetime.fromtimestamp(t)
        Y_M = str(_t)[0:7]
        if does_key_exist(_deploys_by_month, Y_M) == False:
            _deploys_by_month[Y_M] = [deploy[1]]
        else:
            _deploys_by_month[Y_M].append(deploy[1])
    return _deploys_by_month
