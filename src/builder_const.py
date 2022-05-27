from builder_types import *

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
EMERGENCY_ALLOCATION = int(TOTAL_ALLOCATION * 0.005)
EMERGENCY_ALLOCATION_ADDRESS = "terra1cknnv35slav8jnsmywmzn3q8rvh7rmtlm0tsdk"

DENOM_LUNA = 'uluna'
DENOM_UST = 'uusd'
DENOM_AUST = 'aUST'

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
}

BRIDGE_ADDRESSES: AddressMap = {
    'terra13yxhrk08qvdf5zdc9ss5mwsg5sf7zva9xrgwgc': True,  # Shuttle ETH
    'terra1g6llg3zed35nd3mh9zx6n64tfw3z67w2c48tn2': True,  # Shuttle BSC
    'terra1rtn03a9l3qsc0a9verxwj00afs93mlm0yr7chk': True,  # Shuttle HMY
    'terra10nmmwe8r3g99a9newtqa7a75xfgs2e8z87r2sf': True,  # Wormhole
    'terra1gdxfmwcfyrqv8uenllqn7mh290v7dk7x5qnz03': True,  # Anyswap/Multichain
    'terra18hf7422vyyc447uh3wpzm50wzr54welhxlytfg': True,  # Allbridge
    'terra1t74f2ahytt9uje3td2lnyv3fkay2jj2akj7ytv': True,  # Ren
    'terra1qwzdua7928ugklpytdzhua92gnkxp9z4vhelq8': True,  # Synapse
}
