from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.constants import GiftCardStatus
from app.database import get_db, get_session
from app.models import GiftCard
from app.schemas import GiftCardResponse, RedeemRequest

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


@router.post("/{code}/redeem", response_model=GiftCardResponse)
async def redeem_gift_card(code: str, data: RedeemRequest, session: AsyncSession = Depends(get_session)):
    current_ts = datetime.now()

    try:
        gift_card = (
            await session.execute(
                select(GiftCard)
                .where(
                    GiftCard.code == code,
                    GiftCard.status == GiftCardStatus.ACTIVE.value,
                    GiftCard.expires_at > current_ts
                )
                .with_for_update()
            )
        ).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Действующая гифт-карта не найдена')

    if gift_card.balance < data.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Недостаточно средств на гифт-карте')

    gift_card.balance -= data.amount
    gift_card.status = gift_card.status if gift_card.balance > 0 else GiftCardStatus.REDEEMED.value
    gift_card.updated_at = current_ts

    await session.commit()
    return GiftCardResponse.model_validate(gift_card)
