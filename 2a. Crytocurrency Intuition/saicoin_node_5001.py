# Module 1 - Create a Blockchain

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/
# requests==2.18.4
# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash):
        ""
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'transactions':self.transactions,
                 'previous_hash': previous_hash}
        self.transactions = [] #Update to empty list so that no two blocks have same transactions
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transactions(self, amount, sender, receiver):
        self.transactions.append({'sender':sender, 'amount':amount, 'receiver':receiver })
        previous_block = self.get_previous_block()
        return previous_block['index']+1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        return 'Added nodes'

    def replace_chain(self): #consensus
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
            if longest_chain: #if the chain was updated
                self.chain = longest_chain
                return True
        return False
# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for node on Port 5000
node_address = str(uuid4()).replace('-','')
# Creating a Blockchain
blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address,receiver='Saicharan', amount=100)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'address':node_address,
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'transactions':block['transactions'],
                'previous_hash': block['previous_hash']
}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Add transaction to blockchain
@app.route('/add_transaction', methods = ['GET','POST'])
def add_transaction():
    json = request.get_json()
    if not all(key in json for k in ['sender','receiver','amount']):
        return 'Some elements of transaction are missing',400
    index = blockchain.add_transaction(json['sender'],json['recieve'])
    response = {message:f'TX added  to block{index}'}
    return jsonify(response),201

#connecting all nodes
@app.route('/connect_node', methods = ['GET','POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No node',400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All nodes are now connected and now contains the following nodes',
    'total_nodes':list(blockchain.nodes)}
    return jsonify(response),201

#replace chain
@app.route('/replace_chain', methods = ['GET','POST'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_valid:
        response = {'message': 'Chain has been replaced','new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one','actual_chain':blockchain.chain}
    return jsonify(response),200


@app.route('/hello_world', methods = ['GET','POST'])
def hello_world():
	return 'hello'

# Running the app
app.run(host = '0.0.0.0', port = 5001)
