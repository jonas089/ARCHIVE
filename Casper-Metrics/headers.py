# TBD: remove args ( should be handled in lib.py )
from utils.casper import Client
from config import node
import argparse
from utils.storage import File
from utils.filing import filenames, get_blockfile
from statistics import mean, median
from config import start_height, end_height, steps
from termcolor import colored
import os
import time

cli = Client(node, 8888, 7777, 9999)

base_path = './data/blocks/{start_height}-{end_height}-{steps}/'.format(start_height=str(start_height), end_height=str(end_height), steps=str(steps))

# Setup directories
if not os.path.exists(base_path):
    os.mkdir(base_path)

def fetch_blocks(hfrom, hto):
    fname = '{hfrom}-{hto}'.format(hfrom=str(hfrom), hto=str(hto))
    res = []
    failed = []
    for h in range(hfrom, hto + 1):
        try:
            #print("Trying to get Block #", h)
            res.append(cli.get_block(h))
            #print("Ok.")
        except Exception as failed:
            print("FAILED.")
            failed.append(h)
    # V1
    if len(res) < (hto - hfrom):
        exp = hto - hfrom
        print(
        '[Error] Expected Length {exp}, got Length {gt}'.format(exp=str(exp), gt=str(len(res)))
        )

    #print("Result: ", res)
    #print("Failed: ", failed)
    #print("Total F: ", len(failed))

    #V2
    if len(failed) == 0:
        print("[Info] Round was successful: Saving to ./data/deploys")
        f = File(base_path, fname, 'xml')
        f.create()
        f.write(res)

def auto_fetch(hfrom, hto, steps):
    start_time = time.time()
    f = hfrom
    t = hfrom
    t += steps
    _print = 0
    while t <= hto:
        _print += 1
        print('[Info] Starting Round: ', f, '/', hto)
        fetch_blocks(f, t)
        if f == hfrom and str(f)[len(str(f)) - 1] == '0':
            f += 1
        f += steps
        t += steps
        print('[Info] Fetched ', _print, '{VAR} Blocks') # TBD: translate VAR from config
    print("[Result] Time elapsed: ", str(time.time() - start_time), 'seconds')

def count_deploys(hfrom=0, hto=1310000, steps=1000, type='deploy_hashes'):
    total = 0
    f = filenames(hfrom, hto, steps, 'default')
    for _f in f:
        file = get_blockfile(_f, 'default')
        for block in file.read():
            for deploy in block['body'][type]:
                total += 1
    return total

def count_monthly_blocks(hfrom, hto, steps, month):
    f = filenames(hfrom, hto, steps, 'default')
    total = 0
    for _f in f:
        file = get_blockfile(_f, 'default')
        for block in file.read():
            if block['header']['timestamp'][:7] == month:
                total += 1
    return total

def count_monthly_deploys(hfrom, hto, steps, month, type):
    f = filenames(hfrom, hto, steps, 'default')
    total = 0
    for _f in f:
        file = get_blockfile(_f, 'default')
        for block in file.read():
            if block['header']['timestamp'][:7] == month:
                for deploy in block['body'][type]:
                    total += 1
    return total

#[block['header']['timestamp'], block['body'][type]]
def fetch_timestamp_deploy_pairs(hfrom, hto, steps, size, type, appendix):
    total_length = 0
    f = filenames(hfrom, hto, steps, 'default')
    c = 0
    for _f in f:
        print('[Info] Processing File: ', _f)
        res = []
        file = get_blockfile(_f, 'default')
        for block in file.read():
            for deploy in block['body'][type]:
                res.append([block['header']['timestamp'], deploy])
                if len(res) >= size:
                    temp_file = get_blockfile('deploys{c}'.format(c=c), './data/temp/{appendix}'.format(appendix=appendix))
                    temp_file.create()
                    temp_file.write(res)
                    total_length += len(res)
                    res = []
                    print('[Info] Finished round', c)
                    c += 1
        if len(res) != 0:
            temp_file = get_blockfile('deploys{c}'.format(c=c), './data/temp/{appendix}'.format(appendix=appendix))
            temp_file.write(res)
            total_length += len(res)
            res = []
            c += 1
    print('[Info] Total deploys found: ', total_length)
#############################################
############### Testing #####################
#############################################
'''
from costs import total_cost_from_timestamp_deploy_pairs_by_month
def test():

    #get_timestamp_deploy_pairs(0, 1310000, 1000)
    MONTHS=['2021-05', '2021-06', '2021-07', '2021-08',
    '2021-09', '2021-10', '2021-11', '2021-12',
    '2022-01', '2022-02', '2022-03', '2022-04',
    '2022-05', '2022-06', '2022-07', '2022-08',
    '2022-09', '2022-10', '2022-11']
    #print(count_deploys())
    #fetch_timestamp_deploy_pairs(0, 1310000, 1000, 250)
    for MONTH in MONTHS:
        print(colored('[Info] Month:' + MONTH, 'yellow'))
        print(colored('[Result] ' + str(total_cost_from_timestamp_deploy_pairs_by_month(MONTH)) + ' Motes', 'green'))
        print(colored('-'*20, 'magenta'))
#test()
'''

'''

    1. use get_timestamp_deploy_pairs_by_month to get all deploy hashs
    of a given type in a given month.
    2. calculate the total gas consumed in that month
    3. total gas consumed / total blocks = avg. gas per block
    4. compare average gas per block to max. gas available


'''
'''
def test():
    print('[Result] Monthly Blocks: ', str(count_monthly_blocks(0, 1310000, 1000, '2022-05')))
#test()
'''
