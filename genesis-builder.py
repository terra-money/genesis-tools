import sys
import json
import argparse
from typing import TypedDict, List, Tuple, Dict
from functools import reduce

DENOM_LUNA = 'uluna'
DENOM_UST = 'uusd'
DENOM_AUST = 'aUST'

# Typing Definitions


class Coin(TypedDict):
    denom: str
    amount: str


class VestingPeriod(TypedDict):
    length: str
    amount: List[Coin]


class VestingSchedule(TypedDict):
    # 1: genesis unlock
    # 2: 2 year vesting with 6 month cliff
    # 3: 2 year vesting with 1 year cliff
    # 4: 4 year vesting with 1 year cliff
    type: int
    amount: int


class ConsensusBlockParams(TypedDict):
    max_bytes: str
    max_gas: str
    time_iota_ms: str


class ConsensusEvidenceParams(TypedDict):
    max_age_num_blocks: str
    max_age_duration: str
    max_bytes: str


class ConsensusValidatorParams(TypedDict):
    pub_key_types: List[str]


class ConsensusParams(TypedDict):
    block: ConsensusBlockParams
    evidence: ConsensusEvidenceParams
    validator: ConsensusValidatorParams


class GenesisDoc(TypedDict):
    genesis_time: str
    chain_id: str
    initial_height: str
    consensus_params: ConsensusParams
    app_hash: str
    app_state: Dict


class Balance(TypedDict):
    address: str
    coins: List[Coin]


Balances = List[Balance]
VestingScheduleMap = Dict[str, List[VestingSchedule]]
AddressMap = Dict[str, bool]

BLACK_LIST: AddressMap = {
    'terra17xpfvakm2amg962yls6f84z3kell8c5lkaeqfa': True,  # fee collector
    'terra10d07y265gmmuvt4z0w9aw880jnsr700juxf95n': True,  # gov
    'terra1jv65s3grqf6v6jl3dp4t6c9t9rk99cd8pm7utl': True,  # distribution
    'terra1fl48vsnmsdzcv85q5d2q4z5ajdha8yu3nln0mh': True,  # bonded_tokens_pool
    'terra1tygms3xhhs3yv487phx3dw4a95jn7t7l8l07dr': True,  # not_bonded_tokens_pool
    'terra1jgp27m8fykex4e4jtt0l7ze8q528ux2lh4zh0f': True,  # oracle
    'terra1untf85jwv3kt0puyyc39myxjvplagr3wstgs5s': True,  # market
    'terra1vmafl8f3s6uuzwnxkqz0eza47v6ecn0t0yeca7': True,  # treasury
    'terra1yl6hdjhmkf37639730gffanpzndzdpmhgmvf4r': True,  # ibc transfer
    'terra1m3h30wlvsf8llruxtpukdvsy0km2kum8w4ac9q': True,  # mint
    'terra1dp0taj85ruc299rkdvzp4z5pfg6z6swaed74e6': True,  # foundation
    'terra1gr0xesnseevzt3h4nxr64sh5gk4dwrwgszx3nw': True,  # LFG
    'terra13yxhrk08qvdf5zdc9ss5mwsg5sf7zva9xrgwgc': True,  # Shuttle ETH
    'terra1g6llg3zed35nd3mh9zx6n64tfw3z67w2c48tn2': True,  # Shuttle BSC
    'terra1rtn03a9l3qsc0a9verxwj00afs93mlm0yr7chk': True,  # Shuttle HMY
}

EXCHANGE_LIST: AddressMap = {
    'terra1lg640exsqxa6ftsslx05g4ckgsxqacs2xcfy8a': True,  # Upbit
    'terra107kjnz9u7cy8q3gnzn2zd2p0wgujjtkwz747zq': True,  # Upbit
    'terra164z4d0wga5lkwct2kya9c4jse9hfk3s5gc2p2y': True,  # Upbit
    'terra18z4k5g276cjg38lx3nmx3sp6q8p2j4hch7p3tl': True,  # Upbit
    'terra1fpnt5t2094g3amcwdv3akl60jg9uafgtc38px8': True,  # Upbit
    'terra1l5apaz3yesasc3n7zcumm23swy3llq7dk7f453': True,  # Upbit
    'terra1lh4ye74r29kfse33uh7wc6at55jd4fmypevt07': True,  # Upbit
    'terra1mnltzgjvkz3tacfglxrf9r2m8ajmm3pxatf4mv': True,  # Upbit
    'terra1xrm7z6pthwjlqt5mudq0ft57n940m0edtyh79g': True,  # Upbit
    'terra1t28h4fg8gjpggvq985d2zz569qj8hpxnsxcx93': True,  # Upbit
    'terra10ttyrf534hkmup33gajrlpgps2k7ve8chtxzqh': True,  # Upbit
    'terra1pc4mlakc4xv69q666us3fs8kwjlgkhv083rlgl': True,  # Upbit
}

# community pool: 30%
# pre-attack Luna: 35%
# pre-attack aust: 10%
# post-attack Luna: 10%
# post-attack UST: 15%
TOTAL_ALLOCATION = int(1_000_000_000_000_000)
PRE_ATTACK_LUNA = int(TOTAL_ALLOCATION * 0.35)
PRE_ATTACK_AUST = int(TOTAL_ALLOCATION * 0.10)
POST_ATTACK_LUNA = int(TOTAL_ALLOCATION * 0.10)
POST_ATTACK_UST = int(TOTAL_ALLOCATION * 0.15)


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


# 1: genesis unlock
# 2: 2 year vesting with 6 month cliff
# 3: 2 year vesting with 1 year cliff
# 4: 4 year vesting with 1 year cliff
#    |      |  p1  |         p2         |  p3  |            p4             |
# 6m |------|------|------|------|------|------|------|------|------|------|
# t1 |+     |      |      |      |      |      |      |      |      |      |
# t2 |      |++++++|++++++|++++++|++++++|      |      |      |      |      |
# t3 |      |      |++++++|++++++|++++++|++++++|      |      |      |      |
# t4 |      |      |++++++|++++++|++++++|++++++|++++++|++++++|++++++|++++++|

def merge_vesting_schedules(schedules: List[VestingSchedule]) -> Tuple[int, int, int, List[VestingPeriod]]:
    periods: List[VestingPeriod] = []

    total_amount = sum(map(lambda v: v['amount'], schedules))
    unlocked_amount = sum(
        map(lambda v: v['amount'] if v['type'] == 1 else 0, schedules))
    vesting_amount = total_amount - unlocked_amount

    start_time = 60 * 60 * 24 * 30 * 6  # 6 month
    p1_amount = sum(map(lambda v: int(v['amount'] / 4)
                        if v['type'] == 2 else 0, schedules))
    if p1_amount != 0:
        periods.append({
            'length': str(60 * 60 * 24 * 30 * 6),  # 6 month
            'amount': [{'denom': DENOM_LUNA, 'amount': str(p1_amount)}]
        })
    else:
        periods.append({
            'length': str(60 * 60 * 24 * 30 * 6),  # 6 month
            'amount': []
        })

    p2_amount = sum(map(lambda v: v['amount'] - int(v['amount'] / 4)
                        if v['type'] == 2 else int(v['amount'] * 3 / 4)
                        if v['type'] == 3 else int(v['amount'] * 3 / 8)
                        if v['type'] == 4 else 0, schedules))
    if p2_amount != 0:
        periods.append({
            'length': str(60 * 60 * 24 * 30 * 18),  # 18 month
            'amount': [{'denom': DENOM_LUNA, 'amount': str(p2_amount)}],
        })
    else:
        periods.append({
            'length': str(60 * 60 * 24 * 30 * 18),  # 18 month
            'amount': [],
        })

    p3_amount = sum(map(lambda v: v['amount'] - int(v['amount'] * 3 / 4)
                        if v['type'] == 3 else int(v['amount'] / 8)
                        if v['type'] == 4 else 0, schedules))
    if p3_amount != 0:
        periods.append({
            'length': str(60 * 60 * 24 * 30 * 6),  # 6 month
            'amount': [{'denom': DENOM_LUNA, 'amount': str(p3_amount)}],
        })
    else:
        periods.append({
            'length': str(60 * 60 * 24 * 30 * 6),  # 6 month
            'amount': [],
        })

    p4_amount = sum(map(lambda v: v['amount'] - int(v['amount'] / 8) - int(v['amount'] * 3 / 8)
                        if v['type'] == 4 else 0, schedules))
    if p4_amount != 0:
        periods.append({
            'length': str(60 * 60 * 24 * 30 * 24),  # 24 month
            'amount': [{'denom': DENOM_LUNA, 'amount': str(p4_amount)}],
        })
    else:
        periods.append({
            'length': str(60 * 60 * 24 * 30 * 24),  # 24 month
            'amount': [],
        })

    return [str(total_amount), str(vesting_amount), str(start_time), periods]


def process_pre_attack_snapshot(
        pre_attack_snapshot: GenesisDoc,
        vesting_schedule_map: VestingScheduleMap,
        contract_address_map: AddressMap,
) -> int:
    allocation_luna = PRE_ATTACK_LUNA
    allocation_aust = PRE_ATTACK_AUST

    balances: Balances = pre_attack_snapshot['app_state']['bank']['balances']

    total_luna = 0
    total_aust = 0
    luna_holders: Dict[str, int] = {}
    aust_holders: Dict[str, int] = {}
    for balance in balances:
        # filter out blacklist
        if balance['address'] in BLACK_LIST or balance['address'] in contract_address_map:
            continue

        is_exchange = False
        if balance['address'] in EXCHANGE_LIST:
            is_exchange = True

        for coin in balance['coins']:
            if coin['denom'] == DENOM_LUNA:
                amount = int(coin['amount'])
                luna_holders[balance['address']] = amount
                total_luna += amount
            elif coin['denom'] == DENOM_AUST:
                # apply 500K whale cap
                # no whale cap for exchanges
                amount = min(int(coin['amount']), 500_000_000_000) \
                    if not is_exchange else coin['amount']
                aust_holders[balance['address']] = amount
                total_aust += amount

    total_allocation_amount: int = 0

    # allocate luna portion
    for addr, balance in luna_holders.items():
        allocation_amount = int(balance * allocation_luna / total_luna)

        schedules = []
        # for exchanges, no whale condition applied.
        if addr in EXCHANGE_LIST or balance < 10_000_000_000:
            # For wallets with < 10k Luna: 30% unlocked at genesis; 70% vested over 2 years with 6 month cliff
            vesting_amount = int(allocation_amount * 0.7)
            unlock_amount = allocation_amount - vesting_amount
            schedules = [{
                'type': 1,
                'amount': unlock_amount
            }, {
                'type': 2,
                'amount': vesting_amount,
            }]
        elif balance < 1000_000_000_000:
            # For wallets with < 1M Luna: 1 year cliff, 2 year vesting thereafter
            schedules = [{
                'type': 3,
                'amount': allocation_amount,
            }]
        else:
            # For wallets with > 1M Luna: 1 year cliff, 4 year vesting thereafter
            schedules = [{
                'type': 4,
                'amount': allocation_amount,
            }]

        if addr not in vesting_schedule_map:
            vesting_schedule_map[addr] = schedules
        else:
            vesting_schedule_map[addr].extend(schedules)
        total_allocation_amount += allocation_amount

    # allocate aust portion
    for addr, balance in aust_holders.items():
        allocation_amount = int(balance * allocation_aust / total_aust)

        # 30% unlocked at genesis; 70% vested over 2 years thereafter with 6 month cliff
        vesting_amount = int(allocation_amount * 0.7)
        unlock_amount = allocation_amount - vesting_amount

        schedules = [{
            'type': 1,
            'amount': unlock_amount,
        }, {
            'type': 2,
            'amount': vesting_amount,
        }]

        if addr not in vesting_schedule_map:
            vesting_schedule_map[addr] = schedules
        else:
            vesting_schedule_map[addr].extend(schedules)
        total_allocation_amount += allocation_amount

    return total_allocation_amount


def process_post_attack_snapshot(
        post_attack_snapshot: GenesisDoc,
        vesting_schedule_map: VestingScheduleMap,
        contract_address_map: AddressMap,
) -> int:
    allocation_luna = POST_ATTACK_LUNA
    allocation_ust = POST_ATTACK_UST

    balances: Balances = post_attack_snapshot['app_state']['bank']['balances']

    total_luna = 0
    total_ust = 0
    luna_holders: Dict[str, int] = {}
    ust_holders: Dict[str, int] = {}
    for balance in balances:
        # filter out blacklist
        if balance['address'] in BLACK_LIST or balance['address'] in contract_address_map:
            continue

        for coin in balance['coins']:
            if coin['denom'] == DENOM_LUNA:
                amount = int(coin['amount'])
                luna_holders[balance['address']] = amount
                total_luna += amount
            elif coin['denom'] == DENOM_UST:
                amount = int(coin['amount'])
                ust_holders[balance['address']] = amount
                total_ust += amount

    total_allocation_amount: int = 0

    # allocate luna portion
    for addr, balance in luna_holders.items():
        allocation_amount = int(balance * allocation_luna / total_luna)

        # 30% unlocked at genesis; 70% vested over 2 years thereafter with 6 month cliff
        vesting_amount = int(allocation_amount * 0.7)
        unlock_amount = allocation_amount - vesting_amount
        schedules = [{
            'type': 1,
            'amount': unlock_amount
        }, {
            'type': 2,
            'amount': vesting_amount,
        }]

        if addr not in vesting_schedule_map:
            vesting_schedule_map[addr] = schedules
        else:
            vesting_schedule_map[addr].extend(schedules)
        total_allocation_amount += allocation_amount

    # allocate ust portion
    for addr, balance in ust_holders.items():
        allocation_amount = int(balance * allocation_ust / total_ust)

        # 30% unlocked at genesis; 70% vested over 2 years thereafter with 6 month cliff
        vesting_amount = int(allocation_amount * 0.7)
        unlock_amount = allocation_amount - vesting_amount

        schedules = [{
            'type': 1,
            'amount': unlock_amount,
        }, {
            'type': 2,
            'amount': vesting_amount,
        }]

        if addr not in vesting_schedule_map:
            vesting_schedule_map[addr] = schedules
        else:
            vesting_schedule_map[addr].extend(schedules)
        total_allocation_amount += allocation_amount

    return total_allocation_amount


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

    # Gov: change min deposit to 512 LUNA and deposit period to 7days
    genesis['app_state']['gov']['deposit_params'] = {
        'max_deposit_period': '604800s',  # 7days
        'min_deposit': [{
            'denom': DENOM_LUNA,
            'amount': '512000000'
        }],
    }

    # Gov: make tally params quorum to 10%
    genesis['app_state']['gov']['tally_params'] = {
        'quorum': '0.100000000000000000',
        'threshold': '0.500000000000000000',
        'veto_threshold': '0.334000000000000000'
    }

    # Gov: set voting period 7days
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

    pre_attack_snapshot: GenesisDoc = json.loads(
        parsed_args.pre_attack_snapshot.read())
    pre_attack_allocation = process_pre_attack_snapshot(
        pre_attack_snapshot=pre_attack_snapshot,
        vesting_schedule_map=vesting_schedule_map,
        contract_address_map=contract_address_map,
    )

    # explicit clear
    pre_attack_snapshot = None

    post_attack_snapshot: GenesisDoc = json.loads(
        parsed_args.post_attack_snapshot.read())
    post_attack_allocation = process_post_attack_snapshot(
        post_attack_snapshot=post_attack_snapshot,
        vesting_schedule_map=vesting_schedule_map,
        contract_address_map=contract_address_map,
    )

    # explicit clear
    post_attack_snapshot = None

    for address, schedules in vesting_schedule_map.items():
        [total_amount, vesting_amount, start_time,
            periods] = merge_vesting_schedules(schedules)
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

    community_pool_allocation = TOTAL_ALLOCATION - pre_attack_allocation - \
        post_attack_allocation - validator_allocation

    # Distribution: community pool
    genesis['app_state']['distribution']['fee_pool']['community_pool'] = [{
        'denom': DENOM_LUNA,
        'amount': str(community_pool_allocation)
    }]

    # Distribution: set community tax to 0
    genesis['app_state']['distribution']['params'] = {
        "community_tax": "0.000000000000000000",
        "base_proposer_reward": "0.010000000000000000",
        "bonus_proposer_reward": "0.040000000000000000",
        "withdraw_addr_enabled": True
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


def add_normal_account(
    genesis: GenesisDoc,
    address: str,
    amount: str,
):
    genesis['app_state']['auth']['accounts'].append({
        '@type': '/cosmos.auth.v1beta1.BaseAccount',
        'address': address,
        'pub_key': None,
        'account_number': '0',
        'sequence': '0'
    })

    genesis['app_state']['bank']['balances'].append({
        'address': address,
        'coins': [
            {
                'denom': DENOM_LUNA,
                'amount': amount
            }
        ]
    })


def add_module_account(
    genesis: GenesisDoc,
    name: str,
    address: str,
    amount: str,
    permissions: List[str],
):
    genesis['app_state']['auth']['accounts'].append({
        '@type': '/cosmos.auth.v1beta1.ModuleAccount',
        'base_account': {
            'account_number': '0',
            'address': address,
            'pub_key': None,
            'sequence': '0'
        },
        'name':        name,
        'permissions': permissions
    })

    genesis['app_state']['bank']['balances'].append({
        'address': address,
        'coins': [
            {
                'denom': DENOM_LUNA,
                'amount': amount
            }
        ]
    })


def add_continuous_vesting_account(
    genesis: GenesisDoc,
    address: str,
    total_amount: str,
    vesting_amount: str,
    start_time: str,
    end_time: str,
):
    genesis['app_state']['auth']['accounts'].append({
        '@type': '/cosmos.vesting.v1beta1.ContinuousVestingAccount',
        'base_vesting_account': {
            'base_account': {
                'address': address,
                'pub_key': None,
                'account_number': '0',
                'sequence': '0'
            },
            'original_vesting': [
                {
                    'denom': DENOM_LUNA,
                    'amount': vesting_amount
                }
            ],
            'delegated_free': [],
            'delegated_vesting': [],
            'end_time': end_time
        },
        'start_time': start_time
    })

    genesis['app_state']['bank']['balances'].append({
        'address': address,
        'coins': [
            {
                'denom': DENOM_LUNA,
                'amount': total_amount
            }
        ]
    })


def add_delayed_vesting_account(genesis, address, total_amount, vesting_amount, end_time: str):
    genesis['app_state']['auth']['accounts'].append({
        '@type': '/cosmos.vesting.v1beta1.DelayedVestingAccount',
        'base_vesting_account': {
            'base_account': {
                'address': address,
                'pub_key': None,
                'account_number': '0',
                'sequence': '0'
            },
            'original_vesting': [
                {
                    'denom': DENOM_LUNA,
                    'amount': vesting_amount
                }
            ],
            'delegated_free': [],
            'delegated_vesting': [],
            'end_time': end_time
        }
    })

    genesis['app_state']['bank']['balances'].append({
        'address': address,
        'coins': [
            {
                'denom': DENOM_LUNA,
                'amount': total_amount
            }
        ]
    })


def add_periodic_vesting_account(
    genesis: GenesisDoc,
    address: str,
    total_amount: str,
    vesting_amount: str,
    start_time: str,
    vesting_periods: List[VestingPeriod],
):

    def take_length(v: VestingPeriod) -> int:
        return int(v['length'])
    end_time = str(int(start_time) + sum(map(take_length, vesting_periods)))

    genesis['app_state']['auth']['accounts'].append({
        '@type': '/cosmos.vesting.v1beta1.PeriodicVestingAccount',
        'base_vesting_account': {
            'base_account': {
                'address': address,
                'pub_key': None,
                'account_number': '0',
                'sequence': '0'
            },
            'original_vesting': [
                {
                    'denom': DENOM_LUNA,
                    'amount': vesting_amount
                }
            ],
            'delegated_free': [],
            'delegated_vesting': [],
            'end_time': end_time
        },
        'start_time': start_time,
        'vesting_periods': vesting_periods,
    })

    genesis['app_state']['bank']['balances'].append({
        'address': address,
        'coins': [
            {
                'denom': DENOM_LUNA,
                'amount': total_amount
            }
        ]
    })


if __name__ == '__main__':
    parser = init_default_argument_parser(
        prog_desc='Genesis Builder for Terra Revival',
        default_chain_id='phoenix-1',
        default_genesis_time='2022-05-27T06:00:00Z',
        default_pretty=False
    )
    main(parser)
