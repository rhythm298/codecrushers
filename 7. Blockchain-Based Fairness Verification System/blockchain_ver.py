# blockchain_ver.py
from flask import Flask, request, jsonify
from web3 import Web3, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.exceptions import ContractLogicError
import json
import os
from datetime import datetime

app = Flask(__name__)

# Blockchain Configuration
WEB3_PROVIDER = os.getenv('WEB3_PROVIDER', 'http://localhost:7545')
CONTRACT_ABI = json.loads('''[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"player","type":"address"},{"indexed":false,"name":"gameId","type":"uint256"},{"indexed":false,"name":"outcome","type":"string"}],"name":"GameRecorded","type":"event"},{"inputs":[{"name":"_player","type":"address"},{"name":"_gameId","type":"uint256"},{"name":"_outcome","type":"string"}],"name":"recordGame","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getGames","outputs":[{"components":[{"name":"player","type":"address"},{"name":"gameId","type":"uint256"},{"name":"outcome","type":"string"},{"name":"timestamp","type":"uint256"}],"name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}]''')

web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
web3.eth.set_gas_price_strategy(medium_gas_price_strategy)
web3.middleware_onion.add(middleware.time_based_cache_middleware)
web3.middleware_onion.add(middleware.latest_block_based_cache_middleware)

contract_address = '0xYourContractAddress'
contract = web3.eth.contract(address=contract_address, abi=CONTRACT_ABI)

@app.route('/record_game', methods=['POST'])
def record_game():
    try:
        data = request.json
        account = web3.eth.account.privateKeyToAccount(data['privateKey'])
        
        tx = contract.functions.recordGame(
            data['player'],
            int(data['gameId']),
            data['outcome']
        ).buildTransaction({
            'chainId': 1337,
            'gas': 500000,
            'gasPrice': web3.eth.generate_gas_price(),
            'nonce': web3.eth.getTransactionCount(account.address),
        })

        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return jsonify({
            'status': 'success',
            'txHash': tx_hash.hex(),
            'blockNumber': receipt['blockNumber'],
            'timestamp': datetime.now().isoformat()
        }), 201

    except ContractLogicError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/verify_game/<game_id>', methods=['GET'])
def verify_game(game_id):
    events = contract.events.GameRecorded().getLogs(fromBlock=0)
    results = [{
        'player': event.args.player,
        'gameId': event.args.gameId,
        'outcome': event.args.outcome,
        'block': event.blockNumber
    } for event in events if event.args.gameId == int(game_id)]
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
