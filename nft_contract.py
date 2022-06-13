import json
from web3 import Web3, HTTPProvider

# create a web3.py instance w3 by connecting to the local Ethereum node
w3 = Web3(HTTPProvider("http://localhost:8545"))

print(w3.isConnected())

# Initialize a local account object from the private key of a valid Ethereum node address
local_acct = w3.eth.account.from_key("0x4f65b0950f0cbb95585c211733c418479e3ab15d57d9844a46d8c6c138875d08")

# compile your smart contract with truffle first
truffleFile = json.load(open('./nft_lottery/build/contracts/NFT.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# Initialize a contract object with the smart contract compiled artifacts
contract = w3.eth.contract(bytecode=bytecode, abi=abi)

# build a transaction by invoking the buildTransaction() method from the smart contract constructor function
construct_txn = contract.constructor(3000, '0xb95A8c720bbDD408f97CccF07de6ceD493bDbc74').buildTransaction({
    'from': local_acct.address,
    'nonce': w3.eth.getTransactionCount(local_acct.address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})

# sign the deployment transaction with the private key
signed = w3.eth.account.sign_transaction(construct_txn, local_acct.key)

# broadcast the signed transaction to your local network using sendRawTransaction() method and get the transaction hash
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash.hex())

# collect the Transaction Receipt with contract address when the transaction is mined on the network
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Deployed At:", tx_receipt['contractAddress'])
contract_address = tx_receipt['contractAddress']

# Initialize a contract instance object using the contract address which can be used to invoke contract functions
nft = w3.eth.contract(abi=abi, address=contract_address)