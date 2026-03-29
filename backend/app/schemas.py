from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    category: str
    price: Decimal
    currency: str
    description: str | None
    image_url: str | None
    is_available: bool


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total: int
    limit: int
    offset: int


class GiftCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    product_id: UUID
    initial_balance: Decimal
    balance: Decimal
    currency: str
    status: str
    expires_at: datetime | None


class RedeemRequest(BaseModel):
    amount: Decimal
