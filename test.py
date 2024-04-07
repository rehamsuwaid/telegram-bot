from web3 import Web3
from jsonABI import function_signature_to_abi
# Connect to an Ethereum node
web3 = Web3(Web3.HTTPProvider(
    'https://eth.llamarpc.com'))

# Load the contract ABI
contract_address = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
# checksum_address = Web3.to_checksum_address(contract_address)

contract_abi = function_signature_to_abi("balanceOf(address)(uint256)")

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Call a function on the contract
# acc_address = Web3.to_checksum_address(
#     '0x837c20d568dfcd35e74e5cc0b8030f9cebe10a28')
result = contract.functions.balanceOf(
    '0x837c20d568dfcd35e74e5cc0b8030f9cebe10a28').call()

print("Balance:", result)
