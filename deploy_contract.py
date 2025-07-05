from web3 import Web3
import json
import pickle
import sys
import os

from solcx import install_solc
from solcx import compile_source
# add version according to Solidity Code
install_solc(version='0.6.0')


# add ganache_url according to "RPC SERVER" url given in Ganache workspace.
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

def compile_contract(contract_path):
    
    with open(contract_path,"r") as f:
        solidity_code = f.read()
    
    compiled_sol = compile_source(
    solidity_code,
    output_values=['abi', 'bin'],
    solc_version="0.6.0"
    )

    contract_id, contract_interface = compiled_sol.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    return abi,bytecode

def deploy_contract(abi,bytecode,DSO_ADDR):

    EnergyTrading = web3.eth.contract(abi=abi, bytecode=bytecode)

    tx_hash = EnergyTrading.constructor(DSO_ADDR,10).transact({
        'from': DSO_ADDR
    })

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt

if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise TypeError("Too many arguments provided. Expected only 1 arguments.")
    contract_name = sys.argv[1]

    with open("config.json", "r") as f:
        config = json.load(f)

    contract_path = os.path.join(config["contract_path"],contract_name)
    build_path = os.path.join(config["build_path"],contract_name)
    DSO_ADDR = config["dso_address"]

    abi, bytecode = compile_contract(contract_path)
        

    tx_receipt = deploy_contract(abi,bytecode,DSO_ADDR)

    print("Contract deployed Successfully")
    print("Contract Address : ",tx_receipt.contractAddress)

    config["contract_address"] = tx_receipt.contractAddress

    # Save updated config back to file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    with open(os.path.join(build_path,'abi.pkl'), 'wb') as f:
        pickle.dump(abi, f)

    with open(os.path.join(build_path,'bytecode.pkl'), 'wb') as f: 
        pickle.dump(bytecode, f) 
    