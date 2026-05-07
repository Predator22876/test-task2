import uuid

from fastapi import HTTPException


def parse_wallet_id(wallet_id: str) -> uuid.UUID:
    try:
        return uuid.UUID(wallet_id)
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Кошелек не найден",
        )
