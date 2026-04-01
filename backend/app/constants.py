from enum import Enum


class GiftCardStatus(Enum):
    ACTIVE = "active"
    REDEEMED = "redeemed"
    EXPIRED = "expired"
    BLOCKED = "blocked"
