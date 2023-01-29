import pickle
from utils.storage import File
from config import start_height, end_height, steps
import os
blocks_base_path = './data/blocks/{start_height}-{end_height}-{steps}/'.format(start_height=str(start_height), end_height=str(end_height), steps=str(steps))

###################################################
################# EXPORTABLES #####################
###################################################

def get_blockfile(filename, base_path):
    if base_path == 'default':
        base_path = blocks_base_path
    return File(base_path, filename, 'xml')

def filenames(hfrom, hto, steps, base_path):
    if base_path == 'default':
        base_path = blocks_base_path

    f = hfrom
    t = hfrom + steps
    if str(hfrom)[len(str(hfrom)) - 1] == '1':
        t -= 1
    incr = False
    has_incr = False
    filenames = []
    while t <= hto:
        if incr == True:
            f += 1
            has_incr = True
            incr = False
        file = File(base_path, '{f}-{t}'.format(f=f, t=t) , 'xml')
        filenames.append(file.filename)
        f += steps
        t += steps
        if has_incr == False and str(hfrom)[len(str(hfrom)) - 1] == '0':
            incr = True
    return filenames

'''
def count_empty(hfrom, hto, steps):
    if (hto - hfrom) > 100000:
        print("Don't push your luck.")
        return None
    e = []
    f = filenames(hfrom, hto, steps, 'default')
    for _f in f:
        file = get_blockfile(_f, 'default')
        blks = file.read()
        for b in blks:
            if len(b['body']['transfer_hashes']) == 0 and len(b['body']['deploy_hashes']) == 0:
                e.append(b)
    return (e, len(e))
'''
