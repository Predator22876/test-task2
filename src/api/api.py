import uuid
from fastapi import Body, APIRouter

from src.schemas.schemas import OperationType, WalletOperation

router = APIRouter(prefix="/api/v1/wallets", tags=["Операции с кошельком"])

wallets= []

@router.post("") 
async def create_wallet():
    wallet = {"uuid": str(uuid.uuid4()), "balance": 0}
    wallets.append(wallet)
    return wallet

@router.post("/{wallet_id}/operation")
async def perform_operation(
    wallet_id: str, 
    operation: WalletOperation = Body(example={"operation_type": "DEPOSIT", "amount": 100})    
):
    for wallet in wallets:
        if wallet["uuid"] == wallet_id:
            if operation.operation_type == OperationType.DEPOSIT:
                wallet["balance"] += operation.amount
            elif operation.operation_type == OperationType.WITHDRAW:
                wallet["balance"] -= operation.amount
            return wallet
@router.get("/{wallet_id}/balance")
async def get_wallet_balance(wallet_id: str):
    for wallet in wallets:
        if wallet["uuid"] == wallet_id:
            return {"balance": wallet["balance"]}
    return {"error": "Wallet not found"}