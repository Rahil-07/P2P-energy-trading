# ⚡ Blockchain-Based Peer-to-Peer Energy Trading

This project simulates a **decentralized P2P energy trading platform** using **Ethereum smart contracts**, enabling **prosumers** to trade surplus energy directly with **consumers**, regulated by a **DSO (Distribution System Operator)**. It is designed for simulation on a local blockchain using **Ganache** and **Web3.py**.

---

## 📁 Project Structure

```
P2P-energy-trading/
├── contracts/ # Solidity smart contracts
│ └── EnergyTrading.sol
│
├── build/ # Compiled ABI & bytecode
│ └── EnergyTrading/
│     ├── abi.pkl
│     └── bytecode.pkl
│
├── deploy_contract.py # Compiles and deploys the smart contract
├── dso.py # DSO role logic
├── prosumer.py # Prosumer role logic
├── consumer.py # Consumer role logic
│
├── config.json # Runtime configuration (addresses, paths)
└── requirements.txt # Python dependencies
```

---

## 🚦 Roles & Responsibilities

| Role        | Script        | Responsibilities                                       |
| ----------- | ------------- | ------------------------------------------------------ |
| 🛠️ DSO      | `dso.py`      | Registers nodes, matches trades, verifies transactions |
| 🔋 Prosumer | `prosumer.py` | Adds funds, injects energy, checks balance             |
| 🔌 Consumer | `consumer.py` | Adds funds, purchase energy, check account balance     |

All roles interact with the smart contract via **Web3.py** and log smart contract events.

---

## ⚙️ Prerequisites

- Python 3.8+
- [Ganache](https://trufflesuite.com/ganache/) (local Ethereum blockchain)
- [Solidity compiler](https://solcx.readthedocs.io/) via `py-solc-x`

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Rahil-07/P2P-energy-trading.git
cd P2P-energy-trading
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Ganache

- Start Ganache GUI or run ganache-cli

- Note down the RPC URL and account addresses

### 4. Configure Addresses

Update config.json with your Ganache addresses and paths:

```json
{
  "contract_path": "./contracts/",
  "build_path": "./build/",
  "dso_address": "0x...",
  "prosumer_address": "0x...",
  "consumer_address": "0x...",
  "contract_address": ""
}
```

### 5. Compile & Deploy Contract

```bash
python deploy_contract.py EnergyTrading.sol
```

After successful deployment, the contract address will be written to config.json.

## 💼 Role-Based Simulation

You can now run the respective scripts for each stakeholder:

### 🔧 DSO Panel

```bash
python dso.py
```

- Register new nodes

- Match a prosumer with a consumer

- Execute energy trades

- Verify transactions

- View threshold values

### 🔋 Prosumer Panel

```bash
python prosumer.py
```

- Add funds to wallet

- Inject energy into grid

- View energy and account balances

### 🔌 Consumer Panel

```bash
python consumer.py
```

- Add funds to wallet

- View owned energy and balance

## 📜 Smart Contract: EnergyTrading.sol

Written in Solidity 0.6.0, the contract supports:

- Role-based access control

- Ownership and trading of energy units

- Trade matching and verification

- Transparent event logging

```
Contract ABI and bytecode are stored in build/EnergyTrading/.
```

## 🧪 Events Logged

Each interaction emits on-chain events such as:

- OwnershipEvent
- MatchEvent
- EnergyTraded
- BalanceAdded
- EnergyInjected
- TradingLog
- VerificationEvent
- EnergyLossCalculated

These are printed to console for simulation clarity.

## License

This project is licensed under the [MIT License](LICENSE).
