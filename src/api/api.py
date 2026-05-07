import uuid

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.models import WalletOrm
from src.schemas.schemas import OperationType, WalletOperation
from src.utils.utils import parse_wallet_id

router = APIRouter(
    prefix="/api/v1/wallets",
    tags=["Операции с кошельком"],
)

@router.post("")
async def create_wallet(
    db: AsyncSession = Depends(get_db),
):
    wallet = WalletOrm(
        id=uuid.uuid4(),
        balance=0,
    )
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return {
        "uuid": str(wallet.id),
        "balance": wallet.balance,
    }


@router.post("/{wallet_id}/operation")
async def perform_operation(
    wallet_id: str,
    operation: WalletOperation = Body(
        example={
            "operation_type": "DEPOSIT",
            "amount": 100,
        }
    ),
    db: AsyncSession = Depends(get_db),
):
    wallet_uuid = parse_wallet_id(wallet_id)

    stmt = (
        select(WalletOrm)
        .where(WalletOrm.id == wallet_uuid)
        .with_for_update()
    )
    result = await db.execute(stmt)
    wallet = result.scalar_one_or_none()

    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Кошелек не найден",
        )

    if operation.operation_type == OperationType.DEPOSIT:
        wallet.balance += operation.amount
    elif operation.operation_type == OperationType.WITHDRAW:
        if wallet.balance < operation.amount:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Количество средств на кошельке меньше запрашиваемого "
                    "для снятия"
                ),
            )
        wallet.balance -= operation.amount

    await db.commit()
    await db.refresh(wallet)
    return {
        "uuid": str(wallet.id),
        "balance": wallet.balance,
    }


@router.get("/{wallet_id}/balance")
async def get_wallet_balance(
    wallet_id: str,
    db: AsyncSession = Depends(get_db),
):
    wallet_uuid = parse_wallet_id(wallet_id)

    stmt = select(WalletOrm).where(
        WalletOrm.id == wallet_uuid
    )
    result = await db.execute(stmt)
    wallet = result.scalar_one_or_none()
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Кошелек не найден",
        )

    return {
        "uuid": str(wallet.id),
        "balance": wallet.balance,
    }
