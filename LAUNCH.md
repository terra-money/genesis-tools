## Instructions

The following document describes the necessary steps involved that a validator must take in order to prepare `phoenix-1`. The Terra team will post an official updated `penultimate-genesis.json` and `genesis.json` file, but it is recommended that validators execute the following instructions in order to verify the resulting genesis file.

## Timeline (Expected)

* Fri May 27 2022 18:00:00 GMT+0900 (KST)
* Thu May 27 2022 09:00:00 GMT+0000 (UTC)

    Share `preultimate-genesis.json` and start to collect gen_txs from the validators.

* Sat May 28 2022 12:00:00 GMT+0900 (KST)
* Sat May 28 2022 03:00:00 GMT+0000 (UTC)

    Finish collecting gen_txs and build & share `genesis.json`

* Sat May 28 2022 15:00:00 GMT+0900 (KST)
* Sat May 28 2022 06:00:00 GMT+0000 (UTC)

    Launch network

## Snapshot

1. Stop node
```sh
sudo systemctl stop terrad
```

2. Checkout state exporter and install
```sh
git clone https://github.com/terra-money/core-genesis-exporter
cd core-genesis-exporter
git checkout ca57f5108c14fb3bbdf5bec20b2c9d5c4dca2555
make install
```

3. Verify the exporter binary versions
```sh
terrad version --long
name: terra
server_name: terrad
version: ""
commit: ca57f5108c14fb3bbdf5bec20b2c9d5c4dca2555
build_tags: netgo,ledger
go: go version go1.18 darwin/arm64
```

4. Take pre-attack snapshot
```sh
terrad export --height 7544910 > pre-attack-snapshot.json
```

5. Take post-attack snapshot
```sh
terrad export --height 7790000 > post-attack-snapshot.json
```

6. Verify the SHA256 of the (sorted) pre-attack & post-attack export snapshots
```sh
# pre-attack
jq -S -c -M '' pre-attack-snapshot.json | shasum -a 256
0ac0d5b8f7ea49e500d9033687a6720a99818e99280aba8f12f00b39832a0d5c

# post-attack
jq -S -c -M '' post-attack-snapshot.json | shasum -a 256
9d294b300eb3d936d9567eb128bc66651d196b07c37583e2e051b3bced965766
```

## Penultimate Genesis
Assume this steps will be happening in the same machine with [Snapshot](#Snapshot).

1. Checkout genesis builder
```sh
git clone https://github.com/terra-money/genesis-tools
```

2. Move pre-attack and post-attack snapshots into genesis-tools
```sh
mv ./pre-attack-snapshot.json ./post-attack-snapshot.json ./genesis-tools
```

3. Run genesis builder script
```sh
# install dependency
pip3 install bech32
pip3 install python-dateutil

python3 ./src/genesis_builder.py \
    ./genesis-template.json \
    ./pre-attack-snapshot.json \
    ./post-attack-snapshot.json \
    ./genesis-validators.json \
    --genesis-time=2022-05-28T06:00:00.000000Z \
    --chain-id=phoenix-1 \
    > penultimate-genesis.json
```

4. Verify the SHA256 of the (sorted) penultimate-genesis.json
```sh
jq -S -c -M '' penultimate-genesis.json | shasum -a 256
def346f3ef21e5f484c4e8634918d527382115b871786bd794fac5dacdf46c63
```

# GenTx
Assume this steps will be happening in new validator machine with validator setup (`terra init`).

1. Checkout and install Terra 2.0 core 
```sh
# checkout and install
git clone https://github.com/terra-money/core
cd core
git checkout v2.0.0
make install
```

2. Verify the binary version
```sh
terrad version --long
name: terra
server_name: terrad
version: v2.0.0
commit: ea682c41e7e71ba0b182c9e7f989855fb9595885
build_tags: netgo ledger,
go: go version go1.18.2 linux/amd64
```

3. Prepare Environment
```sh
# install or move penultimate-genesis.json to server
wget https://phoenix-genesis.s3.us-west-1.amazonaws.com/penultimate-genesis.json

# move genesis to config location
mv ./penultimate-genesis.json ~/.terra/config/genesis.json
```

4. Execute GenTx
```sh
terrad gentx validator 1000000uluna \
    --chain-id="phoenix-1" \
    --pubkey=$(terrad tendermint show-validator) \
    --min-self-delegation="1"\
    --security-contact="contact@aaa.services" \
    --moniker=AAA \
    --details="Trusted security provider for Terra Network and projects building on Terra." \
    --identity="AAAAAAAAAAAA" \
    --commission-rate="0.1" \
    --commission-max-rate="0.2" \
    --commission-max-change-rate="0.01" \
    --node-id="$(tr -dc 'a-f0-9' < /dev/urandom | head -c40)" \
    --ip="0.0.0.0"
```

5. Upload generated GenTx file to this repository's gentx folder via PR.
```sh
ls ~/.terra/config/gentx/*
```

## Collect GenTxs
Assume this steps will be happening in the same machine with [GenTx](#GenTx).

1. Download gentx files and locate to terra home config.
```sh
git clone https://github.com/terra-money/genesis-tools
cd genesis-tools
mv ./gentx/* ~/.terra/config/gentx/
```

2. Execute collect-gentxs
```sh
terrad collect-gentxs
```

6. Verify the SHA256 of the (sorted) final genesis
```sh
jq -S -c -M '' ~/.terra/config/genesis.json | shasum -a 256
[placeholder]
```

7. Clear persistent peers of ~/.terra/config/config.toml

`collect-gentx` cmd will fill `persistent_peers` with wrong addresses which are defined in each gentx's memo.

```sh
sed -i 's/^persistent_peers = ".*"/persistent_peers = ""/g' ~/.terra/config/config.toml
```

## Launch Network

1. Install genesis.json
```sh
wget https://phoenix-genesis.s3.us-west-1.amazonaws.com/genesis.json
mv ./genesis.json ~/.terra/config/genesis.json
```

2. Setup config
```sh
sed -i 's/minimum-gas-prices = "0uluna"/minimum-gas-prices = "0.15uluna"/g' ~/.terra/config/app.toml

# This will prevent continuous reconnection try. (default P2P_PORT is 26656)
sed -i 's/external_address = ""/external_address = "[YOUR_EXTERNAL_IP_ADDRESS:P2P_PORT]"/g' ~/.terra/config/config.toml
```

3. Execute binary and wait until network launch
```sh
sudo systemctl start terrad
```
