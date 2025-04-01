#Libraries
from web3 import Web3
import time
from datetime import datetime

#Connect to chain network
bsc = "https://bsc-dataseed1.binance.org/"
w3 = Web3(Web3.HTTPProvider(bsc))
print(w3.is_connected())

# Interact with contract
contract_address = "0xabcd"
token_abi = 'get_from_bsc_scan'
contract = w3.eth.contract(address=contract_address, abi=token_abi)

#Fill sender and receiver address, for sender you need to add pk_user
sender_pk = "private_key_user_send"
sender_address = "address_user_send"

recipient_address = "address_user_receive"

#Set if amount of token > 0
amount = w3.to_wei(0, 'ether')

while True:
    try:
        #check
        token_balance = contract.functions.balanceOf(sender_address).call()
        #human = w3.from_wei(token_balance, 'ether')

        if token_balance > amount:

            nonce = w3.eth.get_transaction_count(sender_address)

            transaction = contract.functions.transfer(recipient_address, token_balance).build_transaction({
                'chainId': 56,  # BSC mainnet chain ID
                'gas': 73705,  # Replace with the appropriate gas value
                'gasPrice': w3.eth.gas_price,
                'nonce': nonce,
            })

            signed_txn = w3.eth.account.sign_transaction(transaction, sender_pk)

            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            print(f'Transaction Hash: {tx_hash.hex()}')

        print("< Amount")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Current Time: {current_time}')

        time.sleep(0.5)

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'Current Time: {current_time}')