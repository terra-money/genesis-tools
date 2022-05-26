import csv
import os.path
from builder_types import *

def build_ibc_address_map() -> AddressMap:
    ibc_address_map: AddressMap = {}

    cur_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(cur_dir, './ibc_addresses.csv'), newline='') as csv_file:
        lines = csv.reader(csv_file, delimiter=',')
        next(lines)
        for row in lines:
            address = row[0]
            ibc_address_map[address] = True

        csv_file.close()
    
    return ibc_address_map