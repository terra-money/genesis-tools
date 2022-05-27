import csv
import os.path
from builder_types import *
from bech32 import bech32_decode, bech32_encode

def build_ibc_address_map() -> Tuple[AddressMap, IBCAccountMap]:
    ibc_address_map: AddressMap = {}

    cur_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(cur_dir, './ibc_addresses.csv'), newline='') as csv_file:
        lines = csv.reader(csv_file, delimiter=',')
        next(lines)
        for row in lines:
            address = row[0]
            ibc_address_map[address] = True

        csv_file.close()

    ibc_account_map: IBCAccountMap = {}
    read_and_convert_address(chain_name='sifchain', ibc_account_map=ibc_account_map)
    read_and_convert_address(chain_name='crescent', ibc_account_map=ibc_account_map)
    read_and_convert_address(chain_name='osmo', ibc_account_map=ibc_account_map)
    
    return [ibc_address_map, ibc_account_map]

def read_and_convert_address(chain_name: str, ibc_account_map: IBCAccountMap):

    cur_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(cur_dir, './pre_attack_' + chain_name + '.csv'), newline='') as csv_file:
        lines = csv.reader(csv_file, delimiter=',')
        next(lines)
        for row in lines:
            address = row[1]
            denom = row[2]
            amount = int(float(row[3]) * 1_000_000)
            if amount == 0:
                continue

            # convert hrp to terra
            [_, words] = bech32_decode(address)
            address = bech32_encode("terra", words)

            pre_attack_luna_amount = 0
            if denom == 'LUNA':
                pre_attack_luna_amount = amount

            if address not in ibc_account_map:
                ibc_account_map[address] = {
                    'address': address,
                    'pre_attack_ibc_luna': pre_attack_luna_amount,
                    'post_attack_ibc_luna': 0,
                    'post_attack_ibc_ust': 0,
                    'post_attack_ibc_allocated': False,
                    'pre_attack_ibc_allocated': False,
                }
            else:
                ibc_account_map[address]['pre_attack_ibc_luna'] += pre_attack_luna_amount

        csv_file.close()

    with open(os.path.join(cur_dir, './post_attack_' + chain_name + '.csv'), newline='') as csv_file:
        lines = csv.reader(csv_file, delimiter=',')
        next(lines)
        for row in lines:
            address = row[1]
            denom = row[2]
            amount = int(float(row[3]) * 1_000_000)
            if amount == 0:
                continue

            # convert hrp to terra
            [_, words] = bech32_decode(address)
            address = bech32_encode("terra", words)

            post_attack_luna_amount = 0
            post_attack_ust_amount = 0
            if denom == 'LUNA':
                post_attack_luna_amount = amount
            elif denom == 'UST':
                post_attack_ust_amount = amount

            if address not in ibc_account_map:
                ibc_account_map[address] = {
                    'address': address,
                    'pre_attack_ibc_luna': 0,
                    'post_attack_ibc_luna': post_attack_luna_amount,
                    'post_attack_ibc_ust': post_attack_ust_amount,
                    'post_attack_ibc_allocated': False,
                    'pre_attack_ibc_allocated': False,
                }
            else:
                ibc_account_map[address]['post_attack_ibc_luna'] += post_attack_luna_amount
                ibc_account_map[address]['post_attack_ibc_ust'] += post_attack_ust_amount

        csv_file.close()
