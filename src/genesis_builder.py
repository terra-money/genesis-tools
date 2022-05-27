import sys
import json
import argparse

from typing import List, Dict
from builder_types import *
from builder_const import *
from builder_snapshot import *
from builder_account import *
from exchange.exchange_processor import *
from ibc.ibc_processor import build_ibc_address_map


def init_default_argument_parser(prog_desc, default_chain_id,
                                 default_genesis_time, default_pretty):
    # Load genesis template via argument
    parser = argparse.ArgumentParser(description=prog_desc)

    parser.add_argument(
        'genesis_template',
        help='template genesis.json file',
        type=argparse.FileType('r'), default=sys.stdin,
    )

    parser.add_argument(
        'pre_attack_snapshot',
        help='pre-attack snapshot genesis.json file',
        type=argparse.FileType('r'), default=sys.stdin,
    )

    parser.add_argument(
        'post_attack_snapshot',
        help='post-attack snapshot genesis.json file',
        type=argparse.FileType('r'), default=sys.stdin,
    )

    parser.add_argument(
        'genesis_validators',
        help='genesis validator list json file',
        type=argparse.FileType('r'), default=sys.stdin,
    )

    parser.add_argument('--chain-id', type=str,
                        help='chain id for new genesis', default=default_chain_id)
    parser.add_argument('--genesis-time', type=str,
                        help='genesis time for new genesis', default=default_genesis_time)
    parser.add_argument('--pretty', type=bool,
                        default=default_pretty)
    return parser


def main(argument_parser):
    args = argument_parser.parse_args()
    if args.chain_id.strip() == '':
        sys.exit('chain-id required')

    genesis: GenesisDoc = json.loads(args.genesis_template.read())
    genesis = process_raw_genesis(genesis=genesis, parsed_args=args)

    if args.pretty:
        raw_genesis = json.dumps(genesis, indent=4, sort_keys=True)
    else:
        raw_genesis = json.dumps(genesis, indent=None,
                                 sort_keys=False, separators=(',', ':'))

    print(raw_genesis)


def process_raw_genesis(genesis: GenesisDoc, parsed_args) -> GenesisDoc:

    # ChainID and Genesis Time
    genesis['chain_id'] = parsed_args.chain_id
    genesis['genesis_time'] = parsed_args.genesis_time

    # Consensus Params: Block
    genesis['consensus_params']['block'] = {
        'max_bytes': '1000000',
        'max_gas': '100000000',
        'time_iota_ms': '1000',
    }

    # Consensus Params: Evidence
    genesis['consensus_params']['evidence'] = {
        'max_age_num_blocks': '100000',
        'max_age_duration': '172800000000000',
        'max_bytes': '1000000'
    }

    # Auth: set max memo characters to 512
    genesis['app_state']['auth']['params']['max_memo_characters'] = '512'

    # Bank: setup supply
    genesis['app_state']['bank']['supply'] = [{
        'denom': DENOM_LUNA,
        'amount': str(TOTAL_ALLOCATION),
    }]

    # Bank: set denom meta
    genesis['app_state']['bank']['denom_metadata'] = [{
        'description': 'The native staking token of Terra 2.0',
        'denom_units': [
            {'denom': 'uluna', 'exponent': 0, 'aliases': ['microluna']},
            {'denom': 'mluna', 'exponent': 3, 'aliases': ['milliluna']},
            {'denom': 'luna', 'exponent': 6, 'aliases': []},
        ],
        'base':    'uluna',
        'display': 'luna',
        'name':    'LUNA',
        'symbol':  'LUNA',
    }]

    # Mint: set mint params
    genesis['app_state']['mint'] = {
        'minter': {
            'inflation': '0.070000000000000000',
            'annual_provisions': '0.000000000000000000'
        },
        'params': {
            'mint_denom': DENOM_LUNA,
            'inflation_rate_change': '0.000000000000000000',
            'inflation_max': '0.070000000000000000',
            'inflation_min': '0.070000000000000000',
            'goal_bonded': '0.670000000000000000',
            'blocks_per_year': '4360000'
        }
    }

    # Staking: change bond_denom to uluna and max validators to 130
    genesis['app_state']['staking']['params'] = {
        'unbonding_time': '1814400s',  # 21 days
        'max_validators': 130,
        'max_entries': 7,
        'historical_entries': 10000,
        'bond_denom': DENOM_LUNA
    }

    # Crisis: change constant fee to 512 LUNA
    genesis['app_state']['crisis']['constant_fee'] = {
        'denom': DENOM_LUNA,
        'amount': '512000000',
    }

    # Gov: change min deposit to 512 LUNA and deposit period to 7 days
    genesis['app_state']['gov']['deposit_params'] = {
        'max_deposit_period': '604800s',  # 7days
        'min_deposit': [{
            'denom': DENOM_LUNA,
            'amount': '512000000'
        }],
    }

    # Gov: set tally params quorum to 10%
    genesis['app_state']['gov']['tally_params'] = {
        'quorum': '0.100000000000000000',
        'threshold': '0.500000000000000000',
        'veto_threshold': '0.334000000000000000'
    }

    # Gov: set voting period to 7 days
    genesis['app_state']['gov']['voting_params'] = {
        'voting_period': '604800s'
    }

    # Slashing: slash window setup
    genesis['app_state']['slashing']['params'] = {
        'downtime_jail_duration': '600s',
        'min_signed_per_window': '0.05',
        'signed_blocks_window': '10000',
        'slash_fraction_double_sign': '0.05',  # 5%
        'slash_fraction_downtime': '0.0001'    # 0.01%
    }

    # IBC: restrict allowed client
    genesis['app_state']['ibc']['client_genesis']['params']['allowed_clients'] = [
        '07-tendermint']

    # Auth: clear accounts
    genesis['app_state']['auth']['accounts'] = []

    # Bank: clear balances
    genesis['app_state']['bank']['balances'] = []

    # Genutil: clear gen_txs
    genesis['app_state']['genutil']['gen_txs'] = []

    # Wasm: build contract address map to exclude from snapshot
    contract_address_map = build_contract_address_map(genesis=genesis)

    # Vesting Account Registration with snapshots
    vesting_schedule_map: VestingScheduleMap = {}

    [
        exchange_map,
        exchange_address_name_map,
        exchange_address_map,
    ] = build_exchange_data()

    [
        ibc_address_map,
        ibc_account_map,
    ] = build_ibc_address_map()

    pre_attack_snapshot: GenesisDoc = json.loads(
        parsed_args.pre_attack_snapshot.read())
    pre_attack_allocation = process_pre_attack_snapshot(
        pre_attack_snapshot=pre_attack_snapshot,
        vesting_schedule_map=vesting_schedule_map,
        contract_address_map=contract_address_map,
        exchange_address_map=exchange_address_map,
        exchange_map=exchange_map,
        exchange_address_name_map=exchange_address_name_map,
        ibc_address_map=ibc_address_map,
        ibc_account_map=ibc_account_map,
    )

    # explicit clear
    pre_attack_snapshot = None

    post_attack_snapshot: GenesisDoc = json.loads(
        parsed_args.post_attack_snapshot.read())

    post_attack_allocation = process_post_attack_snapshot(
        post_attack_snapshot=post_attack_snapshot,
        vesting_schedule_map=vesting_schedule_map,
        contract_address_map=contract_address_map,
        exchange_map=exchange_map,
        exchange_address_name_map=exchange_address_name_map,
        ibc_address_map=ibc_address_map,
        ibc_account_map=ibc_account_map,
    )

    # explicit clear
    post_attack_snapshot = None

    for address, schedules in vesting_schedule_map.items():
        [
            total_amount,
            vesting_amount,
            start_time,
            periods,
        ] = merge_vesting_schedules(schedules)

        add_periodic_vesting_account(genesis=genesis, address=address,
                                     total_amount=total_amount, vesting_amount=vesting_amount,
                                     start_time=start_time, vesting_periods=periods)

    # Load genesis validators
    genesis_validators: Dict[str, str] = json.loads(
        parsed_args.genesis_validators.read())
    validator_allocation: int = 0
    for address, amount in genesis_validators.items():

        # Check whether validator address is newly created or not
        if address in vesting_schedule_map:
            print('validator '' + address + '' - already exists')
            exit(-1)

        validator_allocation += int(amount)
        add_normal_account(genesis=genesis, address=address, amount=amount)

    emergency_allocation: int = 0
    if EMERGENCY_ALLOCATION_ADDRESS != None:
        emergency_allocation = EMERGENCY_ALLOCATION
        add_normal_account(
            genesis=genesis,
            address=EMERGENCY_ALLOCATION_ADDRESS,
            amount=emergency_allocation,
        )

    community_pool_allocation = TOTAL_ALLOCATION - pre_attack_allocation - \
        post_attack_allocation - validator_allocation - emergency_allocation

    # Distribution: community pool
    genesis['app_state']['distribution']['fee_pool']['community_pool'] = [{
        'denom': DENOM_LUNA,
        'amount': str(community_pool_allocation)
    }]

    # Distribution: set community tax to 0
    genesis['app_state']['distribution']['params'] = {
        'community_tax': '0.000000000000000000',
        'base_proposer_reward': '0.010000000000000000',
        'bonus_proposer_reward': '0.040000000000000000',
        'withdraw_addr_enabled': True
    }

    # Distribution: module account registration
    add_module_account(
        genesis, 'distribution',
        'terra1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8pm7utl',
        str(community_pool_allocation), [])

    return genesis


def build_contract_address_map(genesis: GenesisDoc) -> AddressMap:
    contract_address_map: AddressMap = {}
    for _, contract in genesis['app_state']['wasm']['contracts']:
        contract_address_map[contract['contract_info']['address']] = True
    return contract_address_map


if __name__ == '__main__':
    parser = init_default_argument_parser(
        prog_desc='Genesis Builder for Terra Revival',
        default_chain_id='phoenix-1',
        default_genesis_time='2022-05-27T06:00:00Z',
        default_pretty=False
    )
    main(parser)
