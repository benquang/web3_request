#Libraries
import requests
import json
import time
import datetime
import pytz

#Get the newest transaction hash from a user when they've done sending BNB
def GetTransBNBToBackendWallet(txs):

    backendWallet = 'wallet_adr_app'

    txhash = 'no'

    current_datetime = datetime.datetime.now()

    date2 = current_datetime.date()
    month_year2 = current_datetime.strftime("%m.%Y")

    for i in range(0, len(txs['result'])):

        timestamp = int(txs['result'][i]['timeStamp'])
        dt = datetime.datetime.fromtimestamp(timestamp)

        date1 = dt.date()
        month_year1 = dt.strftime("%m.%Y")


        if ((txs['result'][i]['to'] == backendWallet) and (txs['result'][i]['value'] == '100000000000000')):

            txhash = txs['result'][i]['hash']
            break

    return txhash

#Execute a request to webapp for receiving award
def SendTxHash(txhash, addr):

    url = 'https://defi-app/api/claiming'

    payload = {
        'txhash': txhash
    }

    json_payload = json.dumps(payload)

    #print(json_payload)

    headers = {
        "Content-Type": "application/json",

        "User-Agent": "PostmanRuntime/7.39.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    try:
      response = requests.post(url, data=json_payload, headers=headers)
    except requests.exceptions.Timeout:
      response = 'Time out'

    return response


module = '?module=account'
action = '&action=txlist'

startblock = '&startblock=0'
endblock = '&endblock=99999999'
page = '&page=1'
offset = '&offset=10'
sort = '&sort=desc'
apikey = '&apikey=get_api_key_from_bscscan'

list_address = [
                'adr_1',
                'adr2',
                'adr3'
]

k = 0
count_not_yet_send = 0
had_has_a_sended = 0


for i in range(0, len(list_address) * 10):

    address = '&address=' + list_address[k]

    txs_url = 'https://api.bscscan.com/api' + module + action + address + startblock + endblock + page + offset + sort + apikey

    response = requests.get(txs_url).text

    txs = json.loads(response)

    txhash = GetTransBNBToBackendWallet(txs)

    if (txhash != 'no'):

        status = SendTxHash(txhash, list_address[k])

        print("Wallet'.", k + 1, ' ', list_address[k])
        print(status)
        print("\n")

        had_has_a_sended = 1

    else:

        status = "Not send BNB yet"

        print("Wallet'.", k + 1, ' ', list_address[k])
        print(status)
        print("\n")

        count_not_yet_send = count_not_yet_send + 1

    if ((count_not_yet_send == len(list_address)) and (had_has_a_sended == 0)):
        time.sleep(10)
        count_not_yet_send = 0

    k = k + 1
    if (k == len(list_address)):
        k = 0

    #time.sleep(45)
