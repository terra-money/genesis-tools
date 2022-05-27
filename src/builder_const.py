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
    'terra1xxx6sc3rfepvr2jzr0tytpvx9dct92gznv5xdx': True,  # Thorchain
    'terra1zxl2ueq7dz04xljh9xzjrs8cgwzg3dktam55kp': True,  # Thorchain
    'terra1sdnrzs8ra763pmq3agy62k2p3wmcfnte43w9sr': True,  # Thorchain
    'terra1u9x46hefczct8n8qh2l5zd3zjx4057fcv2j0tw': True,  # Thorchain
    'terra1xd2f8hlvfx4vdq73904a70vnyq03j4napz5qkt': True,  # Thorchain
    'terra1fwu529njve2hy8wk9d7xs4fq2v6mxlm7fufg9e': True,  # Thorchain
    'terra1gs8vvxclqz7rplk9l4jjzs6ztmr9y5zq9k9t0x': True,  # Thorchain
    'terra1el68x6hagewxamzefha28v3du0fn32m482kmqk': True,  # Thorchain
    'terra1krcz33mejvc5f6grj2c5w5x3kuj7mnjhgrus9c': True,  # Thorchain
    'terra1jcn6ez7w4cdcs9mxdzm4lu9054z3dukehccu8f': True,  # Thorchain
    'terra1kkcfgh8wwqfhfc2hmwf7nrkdexswa0kyhpa3zd': True,  # Thorchain
    'terra159steswryj4tqt6rnttwy8tghns36hw4seh9sx': True,  # Thorchain
    'terra1vdgkmgfud0uy69su9th90hhwlu6gjkx4y9zk5f': True,  # Thorchain
    'terra1v6664w08cnvy9cfltw4pzzfttvwljgawm7d9n8': True,  # Thorchain
    'terra1yzwjdkujv956lx5j2r7a4fk4ajjjm57730ahxg': True,  # Thorchain
    'terra17x539jfnlxm3hjcpd7cn29t3nyn3uv4my2hgr7': True,  # Thorchain
    'terra1jk93saw08vwmqdj684f4w5y6v4dkgdfy234c67': True,  # Thorchain
    'terra1k29hf83nx7jgp764zucevuhz3sg75wfc06sspu': True,  # Thorchain
    'terra1yf4jeq3euekw6uwgukwgtg97zxasxvu7ls0t8g': True,  # Thorchain
    'terra1p4jq8gaq9n24enguz526ahh5tllu336cktgfe4': True,  # Thorchain
    'terra1dum24k9ky5afrp9lprtap5st657gwz6uhl7l5l': True,  # Thorchain
    'terra1c0355gama8pgmdjtnstrshpg2r2lrrg8uk6eaa': True,  # Thorchain
    'terra12hd2keknqm4ddq8e8h2wn4rwu4rz6fmagf4wfz': True,  # Thorchain
    'terra1zn6jxyjgasd5z5j3yvxvyxseprvd4mvssakhap': True,  # Thorchain
    'terra12kkyw6dhtr546yfe22gaqfx9cze50dfjr00j7m': True,  # Thorchain
    'terra1qp8288u08r2da9sj9pkzv3fkh0ugfutklxtm6d': True,  # Thorchain
    'terra17e4uzrfqjxfewldwpqszkcelkj9l2c3qk3jdds': True,  # Thorchain
    'terra1rc936rg4ffp6jn9ddcmwca75crgarsdnz3llxz': True,  # Thorchain
    'terra13s6nzwa926js8x9jjx3sggyr8xw9500g02306q': True,  # Thorchain
    'terra1u5pfv07xtxz6aj59pnejaxh2dy7ew5s79wnu03': True,  # Thorchain
    'terra1ns5h2ed3rksswnc5359hscjv2dr95sxlec9hg5': True,  # Thorchain
    'terra1newujzwu4aek3x0u536dx0yt0ayt3ffa79fwfe': True,  # Thorchain
    'terra15qt4h269d78jyxe4jfjpcnzlg4s0wuamh62m5r': True,  # Thorchain
    'terra1ffpnzky5r44unseradnreh9nrcq0l9fp70x4me': True,  # Thorchain
    'terra1e06hmxf5h43htdn7e3rtsff5xyk84w7e428kzs': True,  # Thorchain
    'terra1zxmxxj9xr2lyuud02mzmupdry3md50daw70r7v': True,  # Thorchain
    'terra1mpsmhp3twv97xcw3j5kmhf2r7u9rrxwe7kwt4y': True,  # Thorchain
    'terra1ejwn32j6ws8femj3fzpzmvtkhlfnjz90r8cmfg': True,  # Thorchain
    'terra1ss9ex4axvwh8e2gzy3jhdx8jsqgs3gzdurawfy': True,  # Thorchain
    'terra1r9qrfv90wwkpgyq48mazsepf5f6vhmhaz5ayg0': True,  # Thorchain
    'terra1jaeem3rqcnw6vweg8q2m5vyht4cyc3vl55anrz': True,  # Thorchain
    'terra170xscqs5d469chdt83fxatjntc79zucrytnj3d': True,  # Thorchain
    'terra1xdwkyz3t7fu7jg5a9nqshe2gueldunj747slcy': True,  # Thorchain
    'terra1yedw5cuz4l93wyj58wdn7s7z8qppfvusljmpd7': True,  # Thorchain
    'terra1n88l0tjqhltx94q7wmxtqyxsa83lnla8cn0avl': True,  # Thorchain
    'terra1errw9wx5pv8rhevexfxa950jx6tux0qywqu4g7': True,  # Thorchain
    'terra1szdphaapkxxf0dah4dj02jyrjkn8rc8plmqzcj': True,  # Thorchain
    'terra1gdtsp32quff4h668ar4q236lkxj0lp8dzw4492': True,  # Thorchain
    'terra1nvw2fhtj9geymzkzyhlggg6rvpq48h2a3383zs': True,  # Thorchain
    'terra1057jq3nlrvz827ncyfxu378ay3uqhwydcqtfen': True,  # Thorchain
    'terra1slnkw42th9tryux32l9r9qg4vx2nnajzvl2trn': True,  # Thorchain
    'terra1z2xacl3uzy92mjmm0rh0deglmvkgpxp5vsckkc': True,  # Thorchain
    'terra1khtj7tmmuxm0mm7sjgem9vndzr66xz4h64xce7': True,  # Thorchain
    'terra1p9vpn7wn0lnhdq6a3nr4frpstxpn09mn2qstsc': True,  # Thorchain
    'terra146hksl6sd8clgytez6637gr5fpfmdejdf98zef': True,  # Thorchain
    'terra1jaegcehmsx952h9zak3gvetewtscu5vzzgyvkl': True,  # Thorchain
    'terra1te7akywfsz5rk978mmah9cfvc02jm7n5x8tqmp': True,  # Thorchain
    'terra1ee5ec0mnvhqvu84lgtxpgcc4yrdhalylfg83z9': True,  # Thorchain
    'terra13mklza5umyxlj8st3v2sl8e6exakpe9w8hzfys': True,  # Thorchain
    'terra1s76zxv0kpr78za293kvj0eep4tfqljacksnf48': True,  # Thorchain
    'terra1z3dmy779shx8x9903ldnyqnt3a3g6vjqxeyvp5': True,  # Thorchain
    'terra1c2z2lp2fdjjsmmxymlnjuadw7wae7n2jrtdrt6': True,  # Thorchain
    'terra1hx3gayvwx0j92nf0ev6c837km4yg4kdk0dej9q': True,  # Thorchain
    'terra12xm549pv0hdyk72nj9j3e6vs8tpcr489j7st2u': True,  # Thorchain
    'terra1scwn3nw4lc9s5nzp39evym6mxn8705gh45mfm7': True,  # Thorchain
    'terra1vevr4l9khpqm5zktk4uqaexv07gewhc6eug2gt': True,  # Thorchain
    'terra1aw876sn7sdyllrzpnp0vekmcqwxnegl2m083j6': True,  # Thorchain
    'terra1hves2hk6zqwr74tz0yvtn8wacm7vzufl2x7hqn': True,  # Thorchain
    'terra1t63ew3e87m3sa0aeqygje92ag62ydlezwjmmug': True,  # Thorchain
    'terra1up84adsyf56huj94cm8k3uz6qtm85znjn4qyad': True,  # Thorchain
    'terra1danuyyrewwqrsv2n74wls323k2x8ngjmg8reca': True,  # Thorchain
    'terra1rf5dc0gq4vsaza6q66xw5297jdpx2xly7q7d8t': True,  # Thorchain
    'terra1xk362wwunmr0gzew05j3euvdkjcvfmfyhcpks4': True,  # Thorchain
    'terra1rxqvnj5whqdwc5aq9f8urenjfme638z6aqw6k8': True,  # Thorchain
    'terra1nueltmqg45xehnfy2zd29falq7k4cnvj2qmavm': True,  # Thorchain
    'terra1kpsyuptekwsf4mmfkmlc4tmpf2td7yfeghcqqw': True,  # Thorchain
    'terra10smhtnkaju9ng0cag5p986czp6vmqvnmnux5eg': True,  # Thorchain
    'terra16ta9xjecs0ju6w4u8f7udh4405lxpvje7a4lyf': True,  # Thorchain
    'terra1ey2753rz6kklxt2tx735k09ultkpfz4pkclv5n': True,  # Thorchain
    'terra1pcylx2quurhr44fg35jgvlrypvag70asztw3uw': True,  # Thorchain
    'terra1xczxhtnu4vmtmkazny5vkdplfm7gtdfwc6qk80': True,  # Thorchain
    'terra12zne4xx0gnhscx2kztct57807mrtfxxspfqckq': True,  # Thorchain
    'terra153qnmh7ev7z6xradw49l4m7gx6ge88hdyevclc': True,  # Thorchain
    'terra1ypjwdplx07vf42qdfkex39dp8zxqnaectnf9cn': True,  # Thorchain
    'terra16l2myl9tlsz3w9kaawt2hjajr5verr9lcg069t': True,  # Thorchain
    'terra10f40m6nv7ulc0fvhmt07szn3n7ajd7e8x5tv0w': True,  # Thorchain
    'terra1kma8d2uxr6edapn48ekhuyzc9t49uws6r8w30e': True,  # Thorchain
    'terra1sw6nfu59rvsfzmzxdgka0puulvy6r89hkxpfsy': True,  # Thorchain
    'terra1faa0c6sqryr0am6ls9u8y6zs22ju2y7ywy38jh': True,  # Thorchain
    'terra12fw3syyy4ff78llh3fvhrvdy7xnqlegvrlatwh': True,  # Thorchain
    'terra1jnf3dwfjanvtdd2g0dhkgzy0yfs6v7vzeupk3m': True,  # Thorchain
    'terra1zqr623vc4xrfnc7h6wxe2xsg7knvx0h23e2ghm': True,  # Thorchain
    'terra18g5uac9dd5f0e9pxjqdj3nqee7z8xlxtuyxgwv': True,  # Thorchain
    'terra13j8meu00n8u52dxx0ukwq2sc08z5qpcr8hs5nq': True,  # Thorchain
    'terra192qypumpq5fk33va8ffgl9ejgujqcvvrkctxtc': True,  # Thorchain
    'terra1a39p456jcetqhy8dls4pnt8l7aqu5f8hxxqpr5': True,  # Thorchain
    'terra1rl9jndu3avht2l4zusw7m8km7uarvth5u08j77': True,  # Thorchain
    'terra1enssn8jaztv6q8quuqnlpw0cge3fnfhqhz56r7': True,  # Thorchain
    'terra1er2c4ml3txvlj5hpzpghtzqp7gfxy7ax6m97kv': True,  # Thorchain
    'terra17ergq7rnhkph6ev62szywfq7vmzwnm7vt9f6m9': True,  # Thorchain
    'terra19ph9mawujd73gvep82pk09pmmsdl35983c49xe': True,  # Thorchain
    'terra1fvjh9x2ln7utkduj4xd67l0g0sz6v53r0nasy6': True,  # Thorchain
    'terra1pmlsgfychtcp7qky9psc6ywlkzp5wwtde7jx05': True,  # Thorchain
    'terra1zwryqce8f68murrc8428cytf38hlayncrknq95': True,  # Thorchain
    'terra1m7tg8nncuyjm0mggmxqgsp8l8lpldrfvygcl0x': True,  # Thorchain
    'terra16ej4s6e25krxrrz73x7m6jhp89m84cup8xpxk3': True,  # Thorchain
    'terra1hsga5e2ul8jsy4t6tnxuqakulhmxs32lnaplah': True,  # Thorchain
    'terra12vq8zqu84s2mxkgf52fwmrc4fv9a62mvf9fn4y': True,  # Thorchain
    'terra1pwz55q79dwwhx5wsa3tucvlpgwj274l3sqvqmr': True,  # Thorchain
    'terra1xd4j3gk9frpxh8r22runntnqy34lwzrdk7py6g': True,  # Thorchain
    'terra1k6yw0r9lrl7r7ne0dszfrw4aeukzyc9z4g5zhf': True,  # Thorchain
    'terra10vmz8d0qwvq5hw9susmf7nefka9usazzc04z2d': True,  # Thorchain
    'terra1jleyj776rzpgkhccd6njqycwdkpt7aklurnpaf': True,  # Thorchain
}
