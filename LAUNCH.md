## Instructions

The following document describes the necessary steps involved that a validator must take in order to prepare `phoenix-1`. The Terra team will post an official updated `penultimate-genesis.json` and `genesis.json` file, but it is recommended that validators execute the following instructions in order to verify the resulting genesis file.

## Timeline (Expected)

* Fri May 26 2022 18:00:00 GMT+0900 (KST)
* Fri May 26 2022 09:00:00 GMT+0000 (UTC)

    Share `preultimate-genesis.json` and start to collect gen_txs from the validators.

* Fri May 28 2022 12:00:00 GMT+0900 (KST)
* Fri May 28 2022 03:00:00 GMT+0000 (UTC)

    Finish collecting gen_txs and build & share `genesis.json`

* Fri May 28 2022 15:00:00 GMT+0900 (KST)
* Fri May 28 2022 06:00:00 GMT+0000 (UTC)

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
make install
```

3. Verify the exporter binary versions
```sh
terrad version --long
core: [placeholder]
git commit: [placeholder]
go.sum hash: [placeholder]
build tags: netgo ledger
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
[placeholder]

# post-attack
jq -S -c -M '' post-attack-snapshot.json | shasum -a 256
[placeholder]
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
python3 ./genesis-builder.py \
    ./genesis-template.json \
    ./pre-attack-snapshot.json \
    ./post-attack-snapshot.json \
    ./genesis-validators.json \
    --genesis-time=2022-05-28T06:00:00.000000Z \
    --pretty=false --chain-id=pheonix-1 \
    > penultimate-genesis.json
```

4. Verify the SHA256 of the (sorted) penultimate-genesis.json
```sh
jq -S -c -M '' penultimate-genesis.json | shasum -a 256
[placeholder]
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
core: v2.0.0
git commit: [placeholder]
go.sum hash: [placeholder]
build tags: netgo ledger
```

3. Prepare Environment
```sh
# install or move penultimate-genesis.json to server
wget [placeholder]

# move genesis to config location
mv ./penultimate-genesis.json ~/.terra/genesis.json
```

4. Execute GenTx
```sh
terrad gentx [key-name] [amount-to-stake] \
    --chain-id phoenix-1 \
    --min-self-delegation=[] \
    --security-contact=[] \
    --moniker=[] \
    --details=[] \
    --commission-rate=[] \
    ...
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

## Launch Network

Execute binary and wait until network launch
```sh
sudo systemctl start terrad
```
