import hashlib
from uuid import uuid4
from fastapi import FastAPI, Request, Response
from blockchain import Blockchain
from node import Node

app = FastAPI()
blockchain = Blockchain()
node = Node()
blockchain.register_node(node)

@app.get("/mine")
async def mine():
    miner = node.identifier
    mining_reward = 1
    last_block = blockchain.last_block
    previous_hash = last_block['previous_hash']
    proof = blockchain.proof_of_work(previous_hash)
    blockchain.new_transaction(
        sender='0',
        recipient=miner,
        amount=mining_reward
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof,previous_hash)
    response = {
        'message': "New block Forged",
        'index': block['index'],
        'transaction': block['transaction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'current_hash': blockchain.hash(block)
    }
    return response

# @app.post("/transactions/new")
# async def new_transaction(info: Request):
#     values = await info.json()
#     required = ['sender','recipient','amount']
#     if not all(k in values for k in required):
#         return Response(content="missing values", status_code=400)
#     index = blockchain.new_transaction(values['sender'],values['recipient'],values['amount'])
#     response = {'message': f'Transaction will be added to Block {index}'}
#     return response

@app.get("/chain")
async def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return response

@app.get("/nodes")
async def full_nodes():
    response = {
        'nodes': blockchain.nodes,
        'length': len(blockchain.nodes)
    }
    return response