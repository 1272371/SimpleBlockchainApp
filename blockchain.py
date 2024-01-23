import datetime as _dt
import hashlib as _hashlib
import json as _json

class Blockchain:
    """
    A simple implementation of a blockchain.

    Attributes:
    - chain (list): A list to store the blocks in the blockchain.

    Methods:
    - __init__(): Initializes the blockchain with a genesis block.
    - mine_block(data: str) -> dict: Mines a new block and adds it to the blockchain.
    - _create_block(data: str, proof: int, previous_hash: str, index: int) -> dict: Creates a new block.
    - get_previous_block() -> dict: Returns the last block in the blockchain.
    - _to_digest(new_proof: int, previous_proof: int, index: int, data: str) -> bytes: Computes the digest for proof of work.
    - _proof_of_work(previous_proof: str, index: int, data: str) -> int: Finds a valid proof of work for a new block.
    - _hash(block: dict) -> str: Computes the cryptographic hash of a block.
    - validate_block(block: dict, previous_block: dict) -> bool: Validates a single block before adding it to the chain.
    - is_chain_valid() -> bool: Validates the entire blockchain, including individual blocks.
    - delete_block(proof: int) -> None: Deletes a block with a given proof from the chain and updates the chain.
    - clear() -> None: Clears the entire chain, leaving only the genesis block.
    """
    def __init__(self):
        """
        Initializes a new blockchain with a genesis block.
        """
        self.chain = list()
        initial_block = self._create_block(
            data="genesis block", proof=1, previous_hash="0", index=1
        )
        self.chain.append(initial_block)

    def mine_block(self, data: str) -> dict:
        """
        Mines a new block with the given data and adds it to the blockchain.

        Args:
        - data (str): The data to be stored in the new block.

        Returns:
        dict: The newly mined block.
        """
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self._proof_of_work(
            previous_proof=previous_proof, index=index, data=data
        )
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(
            data=data, proof=proof, previous_hash=previous_hash, index=index
        )
        self.chain.append(block)
        return block

    def _create_block(
        self, data: str, proof: int, previous_hash: str, index: int
    ) -> dict:
        """
        Creates a new block with the given data, proof, previous hash, and index.

        Args:
        - data (str): The data to be stored in the block.
        - proof (int): The proof of work for the block.
        - previous_hash (str): The hash of the previous block.
        - index (int): The index of the block in the blockchain.

        Returns:
        dict: The newly created block.
        """
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        return block

    def get_previous_block(self) -> dict:
        """
        Returns the last block in the blockchain.

        Returns:
        dict: The last block in the blockchain.
        """
        return self.chain[-1]

    def _to_digest(
        self, new_proof: int, previous_proof: int, index: int, data: str
    ) -> bytes:
        """
        Computes the digest used for proof of work.

        Args:
        - new_proof (int): The new proof to be checked.
        - previous_proof (int): The proof of the previous block.
        - index (int): The index of the block.
        - data (str): The data in the block.

        Returns:
        bytes: The computed digest.
        """
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + data
        return to_digest.encode()

    def _proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        """
        Finds a valid proof of work for a new block.

        Args:
        - previous_proof (str): The proof of the previous block.
        - index (int): The index of the new block.
        - data (str): The data to be stored in the new block.

        Returns:
        int: The valid proof of work.
        """
        new_proof = 1
        check_proof = False

        while not check_proof:
            to_digest = self._to_digest(new_proof, previous_proof, index, data)
            hash_operation = _hashlib.sha256(to_digest).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def _hash(self, block: dict) -> str:
        """
        Computes the cryptographic hash of a block.

        Args:
        - block (dict): The block to be hashed.

        Returns:
        str: The cryptographic hash of the block.
        """
        encoded_block = _json.dumps(block, sort_keys=True).encode()
        return _hashlib.sha256(encoded_block).hexdigest()

    def validate_block(self, block: dict, previous_block: dict) -> bool:
        """
        Validates a single block before adding it to the chain.

        Args:
        - block (dict): The block to be validated.
        - previous_block (dict): The previous block in the chain.

        Returns:
        bool: True if the block is valid, False otherwise.
        """
        if block["previous_hash"] != self._hash(previous_block):
            return False

        previous_proof = previous_block["proof"]
        index, data, proof = block["index"], block["data"], block["proof"]
        hash_operation = _hashlib.sha256(
            self._to_digest(
                new_proof=proof,
                previous_proof=previous_proof,
                index=index,
                data=data,
            )
        ).hexdigest()

        if hash_operation[:4] != "0000":
            return False

        return True

    def is_chain_valid(self) -> bool:
        """
        Validates the entire blockchain, including individual blocks.

        Returns:
        bool: True if the entire blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if not self.validate_block(current_block, previous_block):
                return False

        return True

    def delete_block(self, proof: int) -> None:
        """
        Deletes a block with a given proof from the chain and updates the chain.

        Args:
        - proof (int): The proof of the block to be deleted.

        Returns:
        None
        """
        block_to_delete = None

        for block in self.chain:
            if block["proof"] == proof:
                block_to_delete = block
                break

        if block_to_delete:
            self.chain.remove(block_to_delete)

            for i in range(len(self.chain) - 1, 0, -1):
                current_block = self.chain[i]
                previous_block = self.chain[i - 1]

                current_block["previous_hash"] = self._hash(previous_block)
                current_block["proof"] = self._proof_of_work(
                    previous_proof=previous_block["proof"],
                    index=current_block["index"],
                    data=current_block["data"],
                )
            else:
                print("!FAILED!")

    def clear(self) -> None:
        """
        Clears the entire chain, leaving only the genesis block.

        Returns:
        None
        """
        self.chain = [self.chain[0]]  # Keep only the genesis block
