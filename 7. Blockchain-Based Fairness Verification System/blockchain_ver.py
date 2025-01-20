import hashlib
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory blockchain storage
blockchain = []

def create_block(previous_hash):
    block = {
        'index': len(blockchain) + 1,
        'transactions': [],
        'previous_hash': previous_hash
    }
    blockchain.append(block)
    return block

def hash_block(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    data = request.json
    last_block = blockchain[-1] if blockchain else create_block('0')  # Create genesis block if needed
    transaction = {
        'player_id': data.get('player_id', 'unknown'),
        'game_id': data.get('game_id', 'unknown'),
        'outcome': data.get('outcome', 'pending')
    }
    last_block['transactions'].append(transaction)
    return jsonify({'message': 'Transaction added', 'block_index': last_block['index']}), 201

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify(blockchain), 200

if __name__ == '__main__':
    app.run(debug=True)
