from fastapi import Request
from fastapi.responses import JSONResponse


class BlockchainException(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

@app.exception_handler(BlockchainException)
def handle_blockchain_exception(request: Request, exc: BlockchainException):
    return JSONResponse(content={"error": exc.detail}, status_code=400)