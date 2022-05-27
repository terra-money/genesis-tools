from builder_types import *
from builder_const import *


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

    end_time = str(int(start_time) +
                   sum(map(lambda v: int(v['length']), vesting_periods)))

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
