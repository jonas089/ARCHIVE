# TBD: remove args ( should be handled in lib.py )
from utils.casper import Client
from utils.filing import filenames, get_blockfile
from utils.t1m3st4mps import to_date_time, to_unix, find_earliest_in_timestamp_cost_set, find_latest_in_timestamp_cost_set, convert_timestamps_in_set_to_unix
from utils.plotter import generate
from utils.helper import does_key_exist, deploys_by_month
from utils.statistics import average_deploy_cost_per_month
from config import node
import argparse
from utils.storage import File
from statistics import mean, median
from config import start_height, end_height, steps
import os
import time
import datetime
from termcolor import colored
from tqdm import tqdm

cli = Client(node, 8888, 7777, 9999)
deploy_base_path = './data/deploys/{start_height}-{end_height}-{steps}/'.format(start_height=str(start_height), end_height=str(end_height), steps=str(steps))
transfer_base_path = './data/transfers/{start_height}-{end_height}-{steps}/'.format(start_height=str(start_height), end_height=str(end_height), steps=str(steps))

# Setup directories
if not os.path.exists(deploy_base_path):
    os.mkdir(deploy_base_path)
if not os.path.exists(transfer_base_path):
    os.mkdir(transfer_base_path)


'''
#######################################################
########## Timestamp, Cost - Set(s) ###################
#######################################################
'''


# Download timestamp and cost of all successful deploys of
# a given [type] (deploy_hashes or transfer_hashes).
# Create a new file every [steps] blocks at the given [path]
def fetch_timestamp_cost(hfrom, hto, steps, type, path):
    f = filenames(hfrom, hto, steps, 'default')
    round = 0
    height = 0
    _hfrom = hfrom
    decrement = 0
    total = 0
    failed = 0
    for _f in f:
        if round == 0 and str(hto)[len(str(hto)) - 1] == '0' and str(_hfrom)[len(str(_hfrom)) - 1] == '1':
            decrement = 1
        file = get_blockfile(_f, 'default')
        blks = file.read()
        _from = str(_hfrom+(steps*round))
        _to = str(_hfrom+(steps*round)+steps-decrement)
        new_file_name = '{f}-{t}'.format(f=_from, t=_to)
        res = []
        print('[Info] Round #{f}-{t}'.format(f=_from, t=_to))
        for block in blks:
            _res = []
            for deploy_or_transfer_hash in block['body'][type]:
                total += 1
                _data = None
                _ec = 0
                while _data == None:
                    try:
                        _data = cli.get_deploy(deploy_or_transfer_hash)
                    except Exception as Error:
                        _ec += 1
                        print("ConnError: ", Error, ':', _ec)

                try:
                    _res.append([_data['deploy']['header']['timestamp'], _data['execution_results'][0]['result']['Success']['cost']])
                except Exception as empty:
                    # failed deploys are ignored.
                    if _data['execution_results'][0]['result']['Failure']:
                        #print('Failed deploy.')
                        failed += 1
                    else:
                        print('[Critical] Deploy Data Error!')
                        return
            res.append(_res)
        if round == 0 and str(_hfrom)[len(str(_hfrom)) - 1] == '0':
            _hfrom += 1
            decrement = 1
        ''' Write Block Deploys to a new File
        then increase round and iterate over next block.
        '''
        new_file = File(path, new_file_name, 'xml')
        new_file.create()
        new_file.write(res)

        round += 1
        print('[Result] Total processed hashs: ', total)
        print('[Result] Total failed deploys: ', failed)
    print('[Result] Total Hashes processed: {total}, Failed deploys: {failed}'.format(total=total, failed=failed))
'''
def fetch_all():
    fetch_timestamp_cost(847001, 1310000, steps, 'transfer_hashes', transfer_base_path)
    fetch_timestamp_cost(847001, 1310000, steps, 'deploy_hashes', deploy_base_path)
'''
# retry if ConnError.
# will infinite loop if permanent ConnError.
def get_deploy(d):
    _recv = False
    _deploy = None
    while _recv == False:
        try:
            _deploy = cli.get_deploy(d)
            _recv = True
        except Exception as E:
            #print("[Info] Conn Timeout")
            pass
    if _deploy != None:
        return _deploy
    else:
        return

# set = convert_timestamps_in_set_to_unix(get_timestamp_cost_set(0, 100000, 1000))
# Concerns regarding scalability!
def get_timestamp_cost_set(hfrom, hto, steps, path):
    f = filenames(hfrom, hto, steps, path)
    processed = 0
    timestamp_cost_set = []
    for _f in f:
        file = get_blockfile(_f, path)
        data = file.read()
        for deploy in data:
            processed += 1
            if len(deploy) != 0:
                timestamp_cost_set.append(deploy)
    print("[Info]: Processed ", processed, "Blocks")
    return timestamp_cost_set

# calculate the total gas cost of set returned from "timestamp_deploy_pairs_by_month" ( see headers.py )
def total_cost_from_timestamp_deploy_pairs_by_month(month, _failed, c, appendix):
    total_cost = 0
    total_deploys = 0
    for i in tqdm(range(0,c+1)):
        filename = 'deploys{i}'.format(i=i)
        file = get_blockfile(filename, './data/temp/{appendix}'.format(appendix=appendix))
        set = file.read()
        for pair in set:
            total_deploys += 1
            if pair[0][:7] == month:
                _deploy = get_deploy(pair[1])
                try:
                    total_cost += int(_deploy['execution_results'][0]['result']['Success']['cost'])
                except Exception as failed:
                    if _failed == True:
                        total_cost += int(_deploy['execution_results'][0]['result']['Failure']['cost'])
                    else:
                        print('[Warning]: ', failed)
    print(colored('[Info]: Deploys Processed: ' + str(total_deploys), 'grey'))
    total_deploys = 0
    return total_cost

#######################################################
################## TESTING ############################
#######################################################
# as deploy cost for transfers should be a default constant,
# scan for outliers that consumed more or less gas than usual.

def scan_for_outliers(hfrom, hto, steps, type, month, default):
    outliers = []
    found = False
    f = filenames(hfrom, hto, steps, 'default')
    for _f in f:
        file = get_blockfile(_f, 'default')
        data = file.read()
        for block in data:
            if block['header']['timestamp'][:7] == month:
                for deploy in block['body'][type]:
                    d = get_deploy(deploy)
                    try:
                        c = int(d['execution_results'][0]['result']['Success']['cost'])
                        if c != default:
                            outliers.append(c)
                            if found == False:
                                print('[Info] Found an outlier!')
                                found = True
                    except Exception as failed:
                        c = int(d['execution_results'][0]['result']['Failure']['cost'])
                        if c != default:
                            outliers.append(c)
                            if found == False:
                                print('[Info] Found an outlier!')
                                found = True
    return outliers
def tests():
    #######################################################
    ## Monthly average cost of successful deploys #########
    #######################################################

    # Analyze timestamp:cost pairs
    # a set of SUCCESSFUL deploys ( timestamp : cost )
    set = convert_timestamps_in_set_to_unix(get_timestamp_cost_set(0, 1310000, 1000, deploy_base_path))
    earliest = find_earliest_in_timestamp_cost_set(set)
    latest = find_latest_in_timestamp_cost_set(set)

    print("[Result] Earliest in Set: ", datetime.datetime.fromtimestamp(earliest))
    print("[Result] Latest in Set: ", datetime.datetime.fromtimestamp(latest))
    '''

    '''
    _deploys_by_month = deploys_by_month(set)
    _y = average_deploy_cost_per_month(_deploys_by_month)

    print('-'*15)
    print(_y)
    print("[Result] Successful Deploys: ", len(set))
#tests()
