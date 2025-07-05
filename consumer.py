from web3 import Web3
import json
import pickle
import warnings
warnings.filterwarnings("ignore", message=".*The event signature did not match the provided ABI.*")

ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load config file
with open("config.json", "r") as f:
    config = json.load(f)

CONSUMER_ADDR = config["consumer_address"]
CONTRACT_ADDR = config["contract_address"]

with open('abi.pkl', 'rb') as f:
    abi = pickle.load(f)

EnergyTrading = web3.eth.contract(
    address=CONTRACT_ADDR,
    abi=abi,
)

def add_balance():
    balance = int(input("Enter balance want to add : "))
    
    balance_tx_hash = EnergyTrading.functions.addBalance(balance).transact({'from': CONSUMER_ADDR})
    balance_tx_receipt = web3.eth.wait_for_transaction_receipt(balance_tx_hash)
    print("\nBalance Added successfully.")

    BalanceAdded_log = EnergyTrading.events.BalanceAdded().process_receipt(balance_tx_receipt)
    print("\nevent : \"BalanceAdded\",")
    print(f"args : \n\t{dict(BalanceAdded_log[0]['args'])}\n")

def view_energy_balance():
    ownership = EnergyTrading.functions.ownerships(CONSUMER_ADDR).call()
    print(f"\nYour energy balance: {ownership[1]}")

def view_account_balance():
    balance = EnergyTrading.functions.balances(CONSUMER_ADDR).call()
    print(f"\nYour account balance: {balance}")

# === Menu ===

def menu():
    print("\nConsumer address : ",CONSUMER_ADDR)
    while True:
        print("\n==== Consumer Panel ====")
        print("1. Add Balance")
        print("2. View Energy Balance")
        print("3. View Account Balance")
        print("0. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_balance()
        elif choice == '2':
            view_energy_balance()
        elif choice == '3':
            view_account_balance()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

# === START ===
if __name__ == "__main__":
    menu()