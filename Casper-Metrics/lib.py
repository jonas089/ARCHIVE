from costs import total_cost_from_timestamp_deploy_pairs_by_month, scan_for_outliers
from headers import fetch_timestamp_deploy_pairs, count_monthly_blocks, count_monthly_deploys
from config import start_height, end_height, steps, ascii_art, gas_available
from termcolor import colored
import os

##############################################################
################### ASCII art print ##########################
##############################################################
print(colored(ascii_art, 'red'))

# Setup
def initial_setup():
    # Setup directories
    if not os.path.exists('./data'):
        os.mkdir('./data')
    if not os.path.exists('./data/blocks'):
        os.mkdir('./data/blocks')
    if not os.path.exists('./data/deploys'):
        os.mkdir('./data/deploys')
    if not os.path.exists('./data/transfers'):
        os.mkdir('./data/transfers')

def count_files_in_dir(path):
    return len(os.listdir(path))

##############################################################
############ Analyze Gas consumption in Deploys ##############
##############################################################

# type: either 'deploy_hashes' or 'transfer_hashes'
def generate_dataset_in_temp(type, appendix):
    fetch_timestamp_deploy_pairs(start_height, end_height, steps, 1000, type, appendix)

# example: get_gas_consumed('2022-05')
# c: Amount of Files generated in Temp for this dataset.
# Warning: You can only have a single dataset in ./temp/ at this time.
# This will be changed in a future verison of this tool.
def get_gas_consumed(month, _failed, c, appendix):
    return total_cost_from_timestamp_deploy_pairs_by_month(month, _failed, c, appendix)

##############################################################
##################### TEST FUNCTIONS #########################
##############################################################
def TEST_generate_sets():
    generate_dataset_in_temp('deploy_hashes', 'deploys/')
    generate_dataset_in_temp('transfer_hashes', 'transfers/')

def TEST_deploy_consumption_total():
    MONTHS=['2021-05', '2021-06', '2021-07', '2021-08',
    '2021-09', '2021-10', '2021-11', '2021-12',
    '2022-01', '2022-02', '2022-03', '2022-04',
    '2022-05', '2022-06', '2022-07', '2022-08',
    '2022-09', '2022-10', '2022-11']
    #print(count_deploys())
    #fetch_timestamp_deploy_pairs(0, 1310000, 1000, 250)
    for MONTH in MONTHS:
        print(colored('[Info] Month:' + MONTH, 'yellow'))
        gas = get_gas_consumed(MONTH, True, 1285, 'deploys/')
        print(colored('[Result] ' + str(gas), 'green'))
        print(colored('-'*20, 'magenta'))

        r = ''
        with open('log.txt', 'r') as log:
            r = log.read()
        with open('log.txt', 'w') as log:
            r += '\n' + MONTH + ':' + str(gas)
            log.write(r)
    r = ''
    with open('log.txt', 'r') as log:
        r = log.read()
    with open('log.txt', 'w') as log:
        r += '\n' + '------'
        log.write(r)

    for MONTH in MONTHS:
        print(colored('[Info] Month:' + MONTH, 'yellow'))
        gas = get_gas_consumed(MONTH, True, 1426, 'transfers/')
        print(colored('[Result] ' + str(gas), 'green'))
        print(colored('-'*20, 'yellow'))

        r = ''
        with open('log.txt', 'r') as log:
            r = log.read()
        with open('log.txt', 'w') as log:
            r += '\n' + MONTH + ':' + str(gas)
            log.write(r)
#TEST_generate_sets()
#TEST_deploy_consumption_total()
#print('[Result] Total Transfers: ', count_monthly_deploys(0, 1310000, 1000, '2021-07', 'transfer_hashes'))
#outliers = scan_for_outliers(0,1310000,1000,'transfer_hashes', '2021-07', 10000)
# 0 gas paid by 66 outliers in set 2021-07
#print('[Result] Outliers: ', outliers)
#print('[Result] Outliers (total): ', len(outliers))
count_files_in_dir('./utils')
