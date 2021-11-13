# Bot auto buy token via pancake v2
# Pancakeswap v2: https://bscscan.com/address/0x10ed43c718714eb63d5aa57b78b54704e256024e
# WBNB: https://bscscan.com/token/0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c
# author: quocthanh2694@gmail.com

from pancake import *
from binancesmarchain import *
from web3 import Web3
import json
import config
import time

# Binance smart chain mainnet.
# Notice:
# 1. Edit your private key (senderPrivateKey) and your address (sender_address).
# 2. Edit token to buy (tokenToBuyAddress).
# 3. Edit the amount you want to buy (bnb): bnbAmountToBuy

# Input your info here
# Your wallet info
senderPrivateKey = ''
sender_address = ''

# Address of token to buy
# busd: 0xe9e7cea3dedca5984780bafc599bd69add087d56
tokenToBuyAddress = ''
bnbAmountToBuy = 0.0001


# config
# IMPROTANT: gas is type of string default average is 5
# Increase gas fee to improve transaction speed.
# EX: with gas = 5, BNB price ~ 600u => 1 transaction will cost about:  0.00053534 BNB ($0.34)
gasFeeWei = '5'


# check info
if not senderPrivateKey:
    print('senderPrivateKey can not be null')
    exit()
if not sender_address:
    print('sender_address can not be null')
    exit()
if not tokenToBuyAddress:
    print('tokenToBuyAddress can not be null')
    exit()

# Start bot
# config
print('\n')
web3 = Web3(Web3.HTTPProvider(bsc))
print('web3.isConnected:', web3.isConnected())

# read the balance's sender address
balance = web3.eth.get_balance(sender_address)
read = web3.fromWei(balance, 'ether')
print("BNB Balance:", read)

# busdContract = web3.eth.contract(address=busdAddress, abi=busdabi)
# busd_token_balance = busdContract.balanceOf(sender_address).call()
# print("BUSD Balance:", busd_token_balance)

# input("Input Contract to buy: ")
tokenToBuy = web3.toChecksumAddress(tokenToBuyAddress)

spend = web3.toChecksumAddress(wbnbAddress)

contract = web3.eth.contract(address=panRouterContractAddress, abi=panabi)

# transaction detail
nonce = web3.eth.get_transaction_count(sender_address)

start = time.time()

pancakeswap2_txn = contract.functions.swapExactETHForTokens(
    0,
    [spend, tokenToBuy],
    sender_address,
    (int(time.time()) + 1000)
).buildTransaction({
    'from': sender_address,
    'value': web3.toWei(bnbAmountToBuy, 'ether'),
    'gasPrice': web3.toWei(gasFeeWei, 'gwei'),
    'nonce': nonce,
})

signed_txn = web3.eth.account.sign_transaction(
    pancakeswap2_txn, private_key=senderPrivateKey)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

print('Result Tx:', web3.toHex(tx_token))
print('You can check your result here: ',
      'https://bscscan.com/tx/' + web3.toHex(tx_token))
