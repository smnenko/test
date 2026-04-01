import asyncio
import os
import uuid
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Any, AsyncGenerator
from unittest.mock import MagicMock, AsyncMock

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.exc import NoResultFound

from app.database import get_session
from app.constants import GiftCardStatus
from app.main import app
from app.models import GiftCard


GIFT_CODE = 'BXTY-XXXX-XXXX-XXXX'
DB_NAME = os.getenv('DB_NAME', 'prod')  # для теста race condition

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url='http://test') as c:
        yield c


@pytest_asyncio.fixture
async def mock_db_session() -> AsyncGenerator[AsyncMock, Any]:
    mock = AsyncMock()
    def _override():
        yield mock
    app.dependency_overrides[get_session] = _override
    yield mock
    app.dependency_overrides.pop(get_session, None)


@pytest_asyncio.fixture
async def mock_gift_card(mock_db_session, request) -> AsyncGenerator[AsyncMock, None]:
    mock_gift_card = MagicMock()

    # Простая проверка select-запроса для теста
    if (
        request.param.code != GIFT_CODE or
        request.param.expires_at < datetime.now() or
        request.param.status != GiftCardStatus.ACTIVE.value
    ):
        mock_gift_card.scalar_one.side_effect = NoResultFound()
    else:
        gift_card = request.param
        mock_gift_card.scalar_one.return_value = gift_card

    mock_db_session.execute.return_value = mock_gift_card
    return mock_db_session


@pytest.mark.asyncio
@pytest.mark.parametrize('mock_gift_card', [GiftCard(
    id=uuid.uuid4(),
    product_id=uuid.uuid4(),
    initial_balance=Decimal('100'),
    currency='USD',
    code=GIFT_CODE,
    balance=Decimal('100'),
    status=GiftCardStatus.ACTIVE.value,
    expires_at=datetime.now() + timedelta(days=1),
)], indirect=True)
async def test_redeem_gift_card_success(client, mock_gift_card) -> None:
    response = await client.post(f'/api/gift-cards/{GIFT_CODE}/redeem', json={'amount': 100})
    data = response.json()

    assert response.status_code == 200
    assert data['status'] == 'redeemed'


@pytest.mark.asyncio
@pytest.mark.parametrize('mock_gift_card', [GiftCard(
    id=uuid.uuid4(),
    product_id=uuid.uuid4(),
    initial_balance=Decimal('100'),
    currency='USD',
    code=GIFT_CODE,
    balance=Decimal('100'),
    status=GiftCardStatus.ACTIVE.value,
    expires_at=datetime.now() + timedelta(days=1),
)], indirect=True)
async def test_redeem_gift_card_insufficient_balance(client, mock_gift_card) -> None:
    response = await client.post(f'/api/gift-cards/{GIFT_CODE}/redeem', json={'amount': 100.01})
    data = response.json()

    assert response.status_code == 400
    assert data['detail'] == 'Недостаточно средств на гифт-карте'


@pytest.mark.asyncio
@pytest.mark.parametrize('mock_gift_card', [GiftCard(
    id=uuid.uuid4(),
    product_id=uuid.uuid4(),
    initial_balance=Decimal('100'),
    currency='USD',
    code='BXTY-XXXX-XXXX-XXXY',
    balance=Decimal('100'),
    status=GiftCardStatus.ACTIVE.value,
    expires_at=datetime.now() + timedelta(days=1),
)], indirect=True)
async def test_redeem_gift_card_does_not_exist(client, mock_gift_card) -> None:
    response = await client.post(f'/api/gift-cards/{GIFT_CODE}/redeem', json={'amount': 50})
    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == 'Действующая гифт-карта не найдена'


@pytest.mark.asyncio
@pytest.mark.parametrize('mock_gift_card', [GiftCard(
    id=uuid.uuid4(),
    product_id=uuid.uuid4(),
    initial_balance=Decimal('100'),
    currency='USD',
    code=GIFT_CODE,
    balance=Decimal('100'),
    status=GiftCardStatus.ACTIVE.value,
    expires_at=datetime.now() - timedelta(days=1),
)], indirect=True)
async def test_redeem_gift_card_expired(client, mock_gift_card) -> None:
    response = await client.post(f'/api/gift-cards/{GIFT_CODE}/redeem', json={'amount': 50})
    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == 'Действующая гифт-карта не найдена'


@pytest.mark.asyncio
@pytest.mark.parametrize('mock_gift_card', [GiftCard(
    id=uuid.uuid4(),
    product_id=uuid.uuid4(),
    initial_balance=Decimal('100'),
    currency='USD',
    code=GIFT_CODE,
    balance=Decimal('100'),
    status=GiftCardStatus.BLOCKED.value,
    expires_at=datetime.now() + timedelta(days=1),
)], indirect=True)
async def test_redeem_gift_card_blocked(client, mock_gift_card) -> None:
    response = await client.post(f'/api/gift-cards/{GIFT_CODE}/redeem', json={'amount': 50})
    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == 'Действующая гифт-карта не найдена'


@pytest.mark.asyncio
@pytest.mark.skipif(DB_NAME != 'test', reason='Invalid database environment variables')
async def test_redeem_gift_card_race_condition(client, mock_gift_card) -> None:
    """
    Допускаем, что у нас есть файл settings c переменными окружения БД и например
    переопределяем для ENVIRONMENT=TEST, DB_NAME=test в pytest.ini и тестируем на реальной БД.
    Можно вообще все тесты прогонять на реальной тестовой БД, но это долго.
    """
    responses = await asyncio.gather(
        client.post(f'/api/gift-cards/{GIFT_CODE}/redeem', json={'amount': 100}),
        client.post(f'/api/gift-cards/{GIFT_CODE}/redeem', json={'amount': 100}),
    )
    statuses = (i.status_code for i in responses)

    assert 200 in statuses
    assert 404 in statuses
