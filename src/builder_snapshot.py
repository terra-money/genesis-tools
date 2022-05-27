from builder_types import *
from builder_const import *

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
        exchange_map: ExchangeMap,
        exchange_address_name_map: AddressNameMap,
        exchange_address_map: AddressMap,
        ibc_address_map: AddressMap,
        ibc_account_map: IBCAccountMap,
) -> int:
    allocation_luna = PRE_ATTACK_LUNA
    allocation_aust = PRE_ATTACK_AUST

    balances: Balances = pre_attack_snapshot['app_state']['bank']['balances']

    total_luna = 0
    total_aust = 0
    bridge_luna = 0
    bridge_aust = 0
    ibc_luna = 0
    ibc_aust = 0
    luna_holders: Dict[str, int] = {}
    aust_holders: Dict[str, int] = {}
    for balance in balances:
        address = balance['address']

        # Bridged assets will be funded to community pool.
        # so its amount should be reflected in total
        # but should not be registered as holder
        if address in BRIDGE_ADDRESSES:
            for coin in balance['coins']:
                denom = coin['denom']
                amount = int(coin['amount'])

                if denom == DENOM_LUNA:
                    bridge_luna += amount
                elif denom == DENOM_AUST:
                    bridge_aust += amount

            continue

        # IBC assets will be funded to community pool.
        # so its amount should be reflected in total
        # but should not be registered as holder
        if address in ibc_address_map:
            for coin in balance['coins']:
                denom = coin['denom']
                amount = int(coin['amount'])

                if denom == DENOM_LUNA:
                    ibc_luna += amount
                elif denom == DENOM_AUST:
                    ibc_aust += amount

            continue

        # filter out blacklist
        if address in BLACK_LIST or \
                address in contract_address_map:
            continue

        is_exchange = False
        if address in exchange_address_map:
            is_exchange = True

        # if the address is exchange's representative
        # then add bridged balance to its balance
        exchange: Exchange = None
        if address in exchange_address_name_map:
            name = exchange_address_name_map[address]
            exchange = exchange_map[name]
            exchange['pre_attack_bridged_allocated'] = True

        ibc_account: IBCAccount = None
        if address in ibc_account_map:
            ibc_account = ibc_account_map[address]
            ibc_account['pre_attack_ibc_allocated'] = True

        for coin in balance['coins']:
            denom = coin['denom']
            amount = int(coin['amount'])

            if denom == DENOM_LUNA:
                amount = amount \
                    if exchange == None \
                    else amount + exchange['pre_attack_bridged_luna']
                amount = amount \
                    if ibc_account == None \
                    else amount + ibc_account['pre_attack_ibc_luna']

                luna_holders[address] = amount
                total_luna += amount
            elif denom == DENOM_AUST:
                amount = amount \
                    if exchange == None \
                    else amount + exchange['pre_attack_bridged_aust']

                # apply 500K whale cap
                # no whale cap for exchanges
                amount = min(amount, 500_000_000_000) \
                    if not is_exchange else amount
                aust_holders[address] = amount
                total_aust += amount

    # if the exchange's representative account not exist,
    # then allocation is not conducted so need to manually
    # add holder
    exchange_not_allocated = filter(
        lambda v: not v['pre_attack_bridged_allocated'], exchange_map.values())
    for exchange in exchange_not_allocated:
        address = exchange['address']
        luna_holders[address] = exchange['pre_attack_bridged_luna']
        aust_holders[address] = exchange['pre_attack_bridged_aust']
        total_luna += exchange['pre_attack_bridged_luna']
        total_aust += exchange['pre_attack_bridged_aust']
        exchange['pre_attack_bridged_allocated'] = True

    # if the ibc account not exist, then allocation
    # is not conducted so need to manually add holder
    ibc_accounts_not_allocated = filter(
        lambda v: not v['pre_attack_ibc_allocated'], ibc_account_map.values())
    for ibc_account in ibc_accounts_not_allocated:
        address = ibc_account['address']
        luna_holders[address] = ibc_account['pre_attack_ibc_luna']
        total_luna += ibc_account['pre_attack_ibc_luna']
        ibc_account['pre_attack_ibc_allocated'] = True

    # exchange bridge luna & aust absorbed into
    # exchange's representative address,
    # so need to subtracted from bridge_luna
    exchange_bridge_luna_amount = sum(
        map(lambda v: v['pre_attack_bridged_luna'], exchange_map.values()))
    bridge_luna -= exchange_bridge_luna_amount

    exchange_bridge_aust_amount = sum(
        map(lambda v: v['pre_attack_bridged_aust'], exchange_map.values()))
    bridge_aust -= exchange_bridge_aust_amount

    # ibc accounts are allocated,
    # so need to subtracted from ibc_luna
    ibc_accounts_luna_amount = sum(
        map(lambda v: v['pre_attack_ibc_luna'], ibc_account_map.values()))
    ibc_luna -= ibc_accounts_luna_amount

    # bridge and ibc balance should be reflected to total without holder
    # so that the bridge allocation is sent to community pool
    total_luna += (bridge_luna + ibc_luna)
    total_aust += (bridge_aust + ibc_aust)

    total_allocation_amount: int = 0

    # allocate luna portion
    for addr, balance in luna_holders.items():
        allocation_amount = int(balance * allocation_luna / total_luna)

        # skip tiny amount allocation
        if allocation_amount < 1_000_000:
            continue

        schedules = []
        # for exchanges, no whale condition applied.
        if addr in exchange_address_map or balance < 10_000_000_000:
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

        # skip tiny amount allocation
        if allocation_amount < 1_000_000:
            continue

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
        exchange_map: ExchangeMap,
        exchange_address_name_map: AddressNameMap,
        ibc_address_map: AddressMap,
        ibc_account_map: IBCAccountMap,
) -> int:
    allocation_luna = POST_ATTACK_LUNA
    allocation_ust = POST_ATTACK_UST

    balances: Balances = post_attack_snapshot['app_state']['bank']['balances']

    total_luna = 0
    total_ust = 0
    bridge_luna = 0
    bridge_ust = 0
    ibc_luna = 0
    ibc_ust = 0
    luna_holders: Dict[str, int] = {}
    ust_holders: Dict[str, int] = {}
    for balance in balances:
        address = balance['address']

        # Bridged assets will be funded to community pool (except exchange ones).
        # so its amount should be reflected in total
        # but should not be registered as holder
        if address in BRIDGE_ADDRESSES:
            for coin in balance['coins']:
                denom = coin['denom']
                amount = int(coin['amount'])

                if denom == DENOM_LUNA:
                    bridge_luna += amount
                elif denom == DENOM_UST:
                    bridge_ust += amount

            continue

        # IBC assets will be funded to community pool.
        # so its amount should be reflected in total
        # but should not be registered as holder
        if address in ibc_address_map:
            for coin in balance['coins']:
                denom = coin['denom']
                amount = int(coin['amount'])

                if denom == DENOM_LUNA:
                    ibc_luna += amount
                elif denom == DENOM_UST:
                    ibc_ust += amount

            continue

        # filter out blacklist
        if address in BLACK_LIST or \
                address in contract_address_map:
            continue

        # if the address is exchange's representative
        # then add bridged balance of exchange to its balance
        exchange: Exchange = None
        if address in exchange_address_name_map:
            name = exchange_address_name_map[address]
            exchange = exchange_map[name]
            exchange['post_attack_bridged_allocated'] = True

        ibc_account: IBCAccount = None
        if address in ibc_account_map:
            ibc_account = ibc_account_map[address]
            ibc_account['post_attack_ibc_allocated'] = True

        for coin in balance['coins']:
            denom = coin['denom']
            amount = int(coin['amount'])

            if denom == DENOM_LUNA:
                amount = amount \
                    if exchange == None \
                    else amount + exchange['post_attack_bridged_luna']
                amount = amount \
                    if ibc_account == None \
                    else amount + ibc_account['post_attack_ibc_luna']

                luna_holders[address] = amount
                total_luna += amount
            elif denom == DENOM_UST:
                amount = amount \
                    if exchange == None \
                    else amount + exchange['post_attack_bridged_ust']
                amount = amount \
                    if ibc_account == None \
                    else amount + ibc_account['post_attack_ibc_ust']

                ust_holders[address] = amount
                total_ust += amount

    # if the exchange's representative account not exist,
    # then allocation is not conducted so need to manually
    # add holder
    exchange_not_allocated = filter(
        lambda v: not v['post_attack_bridged_allocated'], exchange_map.values())
    for exchange in exchange_not_allocated:
        address = exchange['address']
        luna_holders[address] = exchange['post_attack_bridged_luna']
        ust_holders[address] = exchange['post_attack_bridged_ust']
        total_luna += exchange['post_attack_bridged_luna']
        total_ust += exchange['post_attack_bridged_ust']
        exchange['post_attack_bridged_allocated'] = True

    # if the ibc account not exist, then allocation
    # is not conducted so need to manually add holder
    ibc_accounts_not_allocated = filter(
        lambda v: not v['post_attack_ibc_allocated'], ibc_account_map.values())
    for ibc_account in ibc_accounts_not_allocated:
        address = ibc_account['address']
        luna_holders[address] = ibc_account['post_attack_ibc_luna']
        ust_holders[address] = ibc_account['post_attack_ibc_ust']
        total_luna += ibc_account['post_attack_ibc_luna']
        total_ust += ibc_account['post_attack_ibc_ust']
        ibc_account['post_attack_ibc_allocated'] = True

    # exchange bridge tokens absorbed into
    # exchange's representative address,
    # so need to subtracted from bridge tokens
    exchange_bridge_luna_amount = sum(
        map(lambda v: v['post_attack_bridged_luna'], exchange_map.values()))
    bridge_luna -= exchange_bridge_luna_amount

    exchange_bridge_ust_amount = sum(
        map(lambda v: v['post_attack_bridged_ust'], exchange_map.values()))
    bridge_ust -= exchange_bridge_ust_amount

    # ibc accounts are allocated,
    # so need to subtracted from ibc_luna
    ibc_accounts_luna_amount = sum(
        map(lambda v: v['post_attack_ibc_luna'], ibc_account_map.values()))
    ibc_luna -= ibc_accounts_luna_amount

    ibc_accounts_ust_amount = sum(
        map(lambda v: v['post_attack_ibc_ust'], ibc_account_map.values()))
    ibc_ust -= ibc_accounts_ust_amount

    # bridge and ibc balance should be reflected to total without holder
    # so that the bridge allocation is sent to community pool
    total_luna += (bridge_luna + ibc_luna)
    total_ust += (bridge_ust + ibc_ust)

    total_allocation_amount: int = 0

    # allocate luna portion
    for addr, balance in luna_holders.items():
        allocation_amount = int(balance * allocation_luna / total_luna)

        # skip tiny amount allocation
        if allocation_amount < 1_000_000:
            continue

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

        # skip tiny amount allocation
        if allocation_amount < 1_000_000:
            continue

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
