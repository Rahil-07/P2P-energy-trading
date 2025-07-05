from web3 import Web3
import json
import pickle
import os
import warnings
warnings.filterwarnings("ignore", message=".*The event signature did not match the provided ABI.*")



ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load config file
with open("config.json", "r") as f:
    config = json.load(f)

build_path = os.path.join(config["build_path"],"EnergyTrading")

DSO_ADDR = config["dso_address"]
CONTRACT_ADDR = config["contract_address"]
PROSUMER_ADDR = config["prosumer_address"]
CONSUMER_ADDR = config["consumer_address"]

with open(f"{build_path}/abi.pkl", 'rb') as f:
    abi = pickle.load(f)

EnergyTrading = web3.eth.contract(
    address=CONTRACT_ADDR,
    abi=abi,
)

def register_node():
    address = input("Enter node address: ")
    role = int(input("Enter role (1 for Prosumer, 2 for Consumer): "))

    register_tx_hash = EnergyTrading.functions.registerNode(address, role).transact({'from': DSO_ADDR})
    register_tx_receipt = web3.eth.wait_for_transaction_receipt(register_tx_hash)
    print("\nNode registered successfully.")

    OwnershipEvent_log = EnergyTrading.events.OwnershipEvent().process_receipt(register_tx_receipt)
    print("\nevent : \"OwnershipEvent\",")
    print(f"args : \n\t{dict(OwnershipEvent_log[0]['args'])})\n")
    # print(OwnershipEvent_log[0]['args'])

def match_prosumer_consumer():
    prosumer = input("Enter prosumer address: ")
    consumer = input("Enter consumer address: ")
    trade_amount = int(input("Enter energy trade amount: "))
    price = int(input("Enter price per unit: "))

    match_tx_hash = EnergyTrading.functions.matchProsumerConsumer(prosumer, consumer, trade_amount, price).transact({'from': DSO_ADDR})
    match_tx_receipt = web3.eth.wait_for_transaction_receipt(match_tx_hash)
    print("\nMatch created successfully.")

    MatchEvent_log = EnergyTrading.events.MatchEvent().process_receipt(match_tx_receipt)
    print("\nevent : \"MatchEvent\",")
    print(f"args : \n\t{dict(MatchEvent_log[0]['args'])}\n")

    EnergyTraded_log = EnergyTrading.events.EnergyTraded().process_receipt(match_tx_receipt)
    print("\nevent : \"EnergyTraded\",")
    print(f"args : \n\t{dict(EnergyTraded_log[0]['args'])}\n")
    

def energy_trading():
    prosumer = input("Enter prosumer address: ")
    consumer = input("Enter consumer address: ")

    trading_tx_hash = EnergyTrading.functions.energyTrading(prosumer, consumer).transact({'from': DSO_ADDR})
    trading_tx_receipt = web3.eth.wait_for_transaction_receipt(trading_tx_hash)
    print("\nEnergy traded successfully.")

    TradingLog_log = EnergyTrading.events.TradingLog().process_receipt(trading_tx_receipt)
    print("\nevent : \"TradingLog\",")
    print(f"args : \n\t{dict(TradingLog_log[0]['args'])}\n")    

def verify_transaction():
    account = input("Enter account address to verify: ")
    tx_type = input("Enter transaction type description (e.g. injection/match/trade): ")

    verify_tx_hash = EnergyTrading.functions.verifyTransaction(tx_type, account).transact({'from': DSO_ADDR})
    verify_tx_receipt = web3.eth.wait_for_transaction_receipt(verify_tx_hash)
    print("\nTransaction verified and event emitted.")

    VerificationEvent_log = EnergyTrading.events.VerificationEvent().process_receipt(verify_tx_receipt)
    print("\nevent : \"VerificationEvent\",")
    print(f"args : \n\t{dict(VerificationEvent_log[0]['args'])}\n")   

def calculate_energy_loss():
    e_source = int(input("Enter source energy : "))
    e_dest = int(input("Enter destination energy : "))

    loss_tx_hash = EnergyTrading.functions.calculateEnergyLoss(e_source,e_dest).transact({'from': DSO_ADDR})
    loss_tx_receipt = web3.eth.wait_for_transaction_receipt(loss_tx_hash)
    print("\nEnergy loss calculated.")

    EnergyLossCalculated_log = EnergyTrading.events.EnergyLossCalculated().process_receipt(loss_tx_receipt)
    print("\nevent : \"EnergyLossCalculated\",")
    print(f"args : \n\t{dict(EnergyLossCalculated_log[0]['args'])}\n") 

def view_threshold_and_dso():
    dso = EnergyTrading.functions.dso().call()
    threshold = EnergyTrading.functions.threshold().call()
    print(f"\nDSO: {dso}")
    print(f"Threshold: {threshold}")

def menu():
    print("\nDSO address : ",DSO_ADDR)
    while True:
        print("\n==== DSO Control Panel ====")
        print("1. Register Node")
        print("2. Match Prosumer and Consumer")
        print("3. Perform Energy Trading")
        print("4. Verify Transaction")
        print("5. Calculate Energy Loss")
        print("6. View DSO & Threshold")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_node()
        elif choice == '2':
            match_prosumer_consumer()
        elif choice == '3':
            energy_trading()
        elif choice == '4':
            verify_transaction()
        elif choice == '5':
            calculate_energy_loss()
        elif choice == '6':
            view_threshold_and_dso()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

# === START ===
if __name__ == "__main__":
    menu()