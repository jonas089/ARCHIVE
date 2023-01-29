import time
import datetime
from utils.filing import filenames, get_blockfile
# functions to parse timestamps of Blocks in dataset
def to_date_time(timestamp):
    date_format = datetime.datetime.strptime(timestamp[:-5],
    "%Y-%m-%dT%H:%M:%S"
    )
    return date_format

def to_unix(timestamp):
    return time.mktime(timestamp.timetuple())

def get_block_timestamps_tuple(hfrom, hto, steps):
    timestamps = []
    _files = filenames(hfrom, hto, steps, 'default')
    for _f in _files:
        _F = get_blockfile(_f, 'default')
        blks = _F.read()
        for blk in blks:
            t = blk['header']['timestamp']
            dtme = to_date_time(t)
            timestamps.append((to_unix(dtme), t))
    return timestamps

def convert_timestamps_in_set_to_unix(timestamp_cost_set):
    data = []
    for pair in timestamp_cost_set:
        for deploy in pair:
            if len(deploy) != 2:
                print("[Error] convert_timestamps_in_set_to_unix: Invalid length!")
                return
            t = deploy[0]
            c = deploy[1]
            data.append([to_unix(to_date_time(t)), c])
    return data

def find_latest_in_timestamp_cost_set(set):
    latest = 0
    for deploy in set:
        if deploy[0] > latest:
            latest = deploy[0]
    return latest

def find_earliest_in_timestamp_cost_set(set):
    earliest = 999999999999999999999999
    for deploy in set:
        if deploy[0] < earliest:
            earliest = deploy[0]
    return earliest
