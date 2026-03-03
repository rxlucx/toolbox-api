from pydantic import BaseModel, Field

class IdempotentRequest(BaseModel):
    idempotency_key: str = Field(..., min_length=8)

class TradeRequest(IdempotentRequest):
    symbol: str
    side: str  # BUY/SELL
    quote_amount: float  # in USDT
    rationale: str = ""

class PostRequest(IdempotentRequest):
    platform: str  # twitter|pinterest|gumroad|notion
    title: str = ""
    body: str
    url: str = ""
    media_urls: list[str] = []