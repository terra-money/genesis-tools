import json
import requests
import csv
import time
from typing import Dict


def fetch_account(account_address):
    r = requests.get(f"https://fcd.terra.dev/v1/txs?account={account_address}&block=7790000&chainId=columbus-5")
    if r.status_code == 200:
        data = r.json()
        return data

def process_addresses(addr):
    try:
        has_balance = fetch_account(addr)
        if has_balance != None and has_balance['txs']:
            print(f"[Error] -> {addr} had a balance ...")
        else:
            # print(f"[+] OK - add: {account_address} val: {to_val_address(account_address)}")
            pass
    except Exception as err:
        print(f"Exception: - {addr} -> {err}")


if __name__ == '__main__':

    with open('genesis-validators.json') as json_file:
        genesis_validators: Dict[str, str] = json.loads(json_file.read())
        for addr, _ in genesis_validators.items():
            process_addresses(addr)
            time.sleep(1)
        print("Done!")