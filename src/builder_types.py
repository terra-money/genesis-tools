from typing import TypedDict, List, Tuple, Dict

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

class Exchange(TypedDict):
    address: str
    pre_attack_bridged_luna: int
    pre_attack_bridged_aust: int
    post_attack_bridged_luna: int
    post_attack_bridged_ust: int
    pre_attack_bridged_allocated: bool
    post_attack_bridged_allocated: bool

Balances = List[Balance]
VestingScheduleMap = Dict[str, List[VestingSchedule]]
AddressMap = Dict[str, bool]
AddressNameMap = Dict[str, str]
ExchangeMap = Dict[str, Exchange]
