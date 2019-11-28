from bitcoin.rpc import RawProxy
import sys



if (len(sys.argv) > 1):
    txid = sys.argv[1]
else:
    txid = "0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2"

def calculate_tx_fee(txid):
    p = RawProxy()

    decoded_tx = p.decoderawtransaction(p.getrawtransaction(txid))

    out_value = 0
    # Retrieve each of the outputs from the transaction
    for output in decoded_tx['vout']:
        #print(output['scriptPubKey']['addresses'], output['value'])
        out_value += output['value']


    inp_value = 0
    for output in decoded_tx['vin']:
        # get 'vin' tx
        inp_txid = output['txid']

        inp_vout_index = output['vout']

        decoded_inp_tx = p.decoderawtransaction(p.getrawtransaction(inp_txid))

        inp_value += decoded_inp_tx['vout'][inp_vout_index]['value']

    return inp_value - out_value

print("Payment = ", calculate_tx_fee(txid))
