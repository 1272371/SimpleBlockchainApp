import fastapi as _fastapi
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import blockchain as _blockchain
import Exception as _Exception


blockchain = _blockchain.Blockchain()
app = _fastapi.FastAPI()

class MineBlockRequest(BaseModel):
    data: str

@app.post("/mine_block/")
def mine_block(request: MineBlockRequest):
    """
    Mine a new block and add it to the blockchain.

    Parameters:
    - request: MineBlockRequest - The request payload containing the data for the new block.

    Returns:
    - dict: The newly mined block.
    """
    if not blockchain.is_chain_valid():
        return JSONResponse(status_code=400, content={"error": "The blockchain is invalid"})
    
    block = blockchain.mine_block(data=request.data)
    return block

@app.get("/blockchain/")
def get_blockchain():
    """
    Retrieve the entire blockchain.

    Returns:
    - list: The list of blocks in the blockchain.
    """
    if not blockchain.is_chain_valid():
        return JSONResponse(status_code=400, content={"error": "The blockchain is invalid"})
    
    return blockchain.chain

@app.get("/validate/")
def is_blockchain_valid():
    """
    Check if the blockchain is valid.

    Returns:
    - dict: A JSON response indicating whether the blockchain is valid.
    """
    return {"valid": blockchain.is_chain_valid()}

@app.get("/blockchain/last/")
def previous_block():
    """
    Retrieve the last block in the blockchain.

    Returns:
    - dict: The last block in the blockchain.
    """
    if not blockchain.is_chain_valid():
        return JSONResponse(status_code=400, content={"error": "The blockchain is invalid"})
        
    return blockchain.get_previous_block()

from fastapi import Depends

def validate_blockchain():
    if len(blockchain.chain)==1:
        raise _Exception.BlockchainException("Nothing to clear, only the genesis!")

@app.post("/clear")
def clear_chain(dependency: str = Depends(validate_blockchain)):
    """
    Endpoint to clear the entire chain, leaving only the genesis block.

    Returns:
    str: A message indicating the success or failure of the operation.
    """
    blockchain.clear()
    return {"message": "Chain cleared successfully"}

@app.post("/delete_block")
def delete_block(request: dict):
    """
    Endpoint to delete a block with a given proof from the chain and update the chain.

    JSON Request Format:
    {
        "proof": 123
    }

    Returns:
    str: A message indicating the success or failure of the operation.
    """
    if 'proof' not in request:
        return JSONResponse(content={'error': 'Proof not provided'}, status_code=400)

    proof_to_delete = request['proof']

    try:
        blockchain.delete_block(proof_to_delete)
        return {"message": "Block deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
