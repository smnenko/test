from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import GiftCard
from app.schemas import GiftCardResponse

router = APIRouter(prefix="/api/gift-cards", tags=["gift-cards"])


@router.get("", response_model=list[GiftCardResponse])
async def get_gift_cards(
    status: str | None = Query(None, description="Фильтр по статусу"),
    db: AsyncSession = Depends(get_db),
):
    """Получить список всех гифт-карт."""
    query = select(GiftCard)
    if status:
        query = query.where(GiftCard.status == status)
    query = query.order_by(GiftCard.created_at.desc())
    result = await db.execute(query)
    cards = result.scalars().all()
    return [GiftCardResponse.model_validate(c) for c in cards]


@router.get("/{code}", response_model=GiftCardResponse)
async def get_gift_card(
    code: str,
    db: AsyncSession = Depends(get_db),
):
    """Получить гифт-карту по коду."""
    result = await db.execute(select(GiftCard).where(GiftCard.code == code))
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Гифт-карта не найдена")
    return GiftCardResponse.model_validate(card)


# TODO: Реализуйте эндпоинт для применения (списания) баланса гифт-карты
# POST /api/gift-cards/{code}/redeem
#
# Входные данные: { "amount": float }
#
# Требования:
# - Проверить что карта существует, активна и не просрочена
# - Проверить что баланс достаточен
# - Списать указанную сумму
# - Вернуть обновленные данные карты
#
