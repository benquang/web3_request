# I. Request to API Endpoints

This part using api key on bscscan to get the transation hash and use it to make a request to the DeFi App' API Endpoints.

Login to bsc with your account and get the api key from bscscan:
```swift
apikey = '&apikey=get_api_key_from_bscscan'

txs_url = 'https://api.bscscan.com/api' + module + action + address + startblock + endblock + page + offset + sort + apikey
```
Get the newest transaction hash from a user when they've done sending 0.0001 BNB to backend wallet address:
```swift
if ((txs['result'][i]['to'] == backendWallet) and (txs['result'][i]['value'] == '100000000000000')):

    txhash = txs['result'][i]['hash']
```
After get the transaction hash, make a request POST to API Endpoints:
```swift
url = 'https://defi-app/api/claiming'

payload = {
    'txhash': txhash
}

try:
    response = requests.post(url, data=json_payload, headers=headers)
except requests.exceptions.Timeout:
    response = 'Time out'
```

# II. Interact with web3 to make a bot auto sending

Connect to chain network:
```swift
bsc = "https://bsc-dataseed1.binance.org/"
w3 = Web3(Web3.HTTPProvider(bsc))
print(w3.is_connected())
```

Interact with contract, you need to get token api on bscscan:
```swift
contract_address = "0xabcd"
token_abi = 'get_from_bsc_scan'
contract = w3.eth.contract(address=contract_address, abi=token_abi)
```

Configure sender and receiver address:
```swift
sender_pk = "private_key_user_send"
sender_address = "address_user_send"

recipient_address = "address_user_receive"
```
The code check if sending user has any amount of token address (>0) then web3 do a funtion `transfer` to receiving user with `token_balance`, configure `gas` for the transaction:
```swift
amount = w3.to_wei(0, 'ether')

if token_balance > amount:
                transaction = contract.functions.transfer(recipient_address, token_balance).build_transaction({
                'chainId': 56,  # BSC mainnet chain ID
                'gas': 73705,  # Replace with the appropriate gas value
                'gasPrice': w3.eth.gas_price,
                'nonce': nonce,
            })
```

We choose each time check sender balance is 0.5 seconds, when transaction is successfull, print the transaction hash:
```swift
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f'Transaction Hash: {tx_hash.hex()}')
```
