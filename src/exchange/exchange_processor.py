import csv
import os.path
from builder_types import *


def build_exchange_data() -> Tuple[ExchangeMap, AddressNameMap, AddressMap]:
    exchange_map: ExchangeMap = {}
    exchange_address_map: AddressMap = {}

    cur_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(cur_dir, './exchange_addresses.csv'), newline='') as csv_file:
        lines = csv.reader(csv_file, delimiter=',')
        next(lines)
        for row in lines:
            name = row[0]
            address = row[2]

            # register first address as representative 
            # address for exchange to receive bridged tokens
            if name not in exchange_map:
                exchange_map[name] = {
                    'address': address,
                    'post_attack_bridged_ust': 0,
                    'pre_attack_bridged_luna': 0,
                    'post_attack_bridged_luna': 0,
                    'pre_attack_bridged_ust': 0,
                    'post_attack_bridged_allocated': False,
                    'pre_attack_bridged_allocated': False,
                }

            exchange_address_map[address] = True

        csv_file.close()

    with open(os.path.join(cur_dir, './pre_attack_non_terra.csv'), newline='') as csv_file:
        lines = csv.reader(csv_file, delimiter=',')
        next(lines)
        for row in lines:
            name = row[0]
            denom = row[7]
            amount = int(float(row[8]) * 1_000_000)
            
            if name not in exchange_map:
                print('no terra address found for ' + name)
                exit(-1)
            
            if denom == 'UST':
                exchange_map[name]['pre_attack_bridged_ust'] += amount
            elif denom == 'LUNA':
                exchange_map[name]['pre_attack_bridged_luna'] += amount
        
        csv_file.close()

    with open(os.path.join(cur_dir, './post_attack_non_terra.csv'), newline='') as csv_file:
        lines = csv.reader(csv_file, delimiter=',')
        next(lines)
        for row in lines:
            name = row[0]
            denom = row[7]
            amount = int(float(row[8]) * 1_000_000)
            
            if name not in exchange_map:
                print('no terra address found for ' + name)
                exit(-1)
            
            if denom == 'UST':
                exchange_map[name]['post_attack_bridged_ust'] += amount
            elif denom == 'LUNA':
                exchange_map[name]['post_attack_bridged_luna'] += amount

        csv_file.close()

    exchange_address_name_map: AddressNameMap = {}
    for name, data in exchange_map.items():
        exchange_address_name_map[data['address']] = name

    return [exchange_map, exchange_address_name_map, exchange_address_map]