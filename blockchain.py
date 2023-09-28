import json
import hashlib
from time import time
from node import Node

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transaction = []
        self.nodes = {}
        self.new_block(734,'Shlapak')

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transaction': self.transaction,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }
        self.transaction = []
        self.chain.append(block)
        return block

    def register_node(self, node: Node):
        self.nodes[node.identifier] = node
        return "Node successfully registered"
    def new_transaction(self,sender, recipient, amount):
        self.transaction.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount
        }
        )
        if sender != '0':
            self.nodes.get(sender).get_reward(-amount);
            self.nodes.get(recipient).get_coin(amount);
        else:
            self.nodes.get(recipient).get_coin(amount);
        return self.last_block['index']+1

    def proof_of_work(self,previous_hash):
        proof = 0
        while self.valid_proof(previous_hash,proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(previous_hash,proof):
        guess = f'{previous_hash}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0703"

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
