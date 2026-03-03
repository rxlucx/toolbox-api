import json
from fastapi import FastAPI, HTTPException
from app.db import get_conn
from app.models import TradeRequest, PostRequest
from app.settings import settings

app = FastAPI(title="Toolbox API", version="0.1.0")

@app.get("/health")
def health():
    return {"ok": True}

def log_event(kind: str, idem: str | None, payload: dict, status: str, result: dict | None = None):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO events(kind,idempotency_key,payload_json,status,result_json) VALUES(?,?,?,?,?)",
            (kind, idem, json.dumps(payload, ensure_ascii=False), status, json.dumps(result, ensure_ascii=False) if result else None)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # Duplicate idempotency key: treat as already done
        raise HTTPException(status_code=409, detail="Duplicate idempotency_key")
    finally:
        conn.close()

@app.post("/trade/spot")
def trade_spot(req: TradeRequest):
    # Guardrails enforced here (Toolbox is the gatekeeper)
    if not settings.TRADING_ENABLED:
        log_event("trade_spot", req.idempotency_key, req.model_dump(), "rejected", {"reason":"TRADING_DISABLED"})
        raise HTTPException(status_code=403, detail="Trading disabled")

    allow = {s.strip().upper() for s in settings.SYMBOL_ALLOWLIST.split(",") if s.strip()}
    symbol = req.symbol.upper()
    if symbol not in allow:
        log_event("trade_spot", req.idempotency_key, req.model_dump(), "rejected", {"reason":"SYMBOL_NOT_ALLOWED"})
        raise HTTPException(status_code=400, detail="Symbol not allowed")

    if req.quote_amount <= 0 or req.quote_amount > settings.MAX_USDT_PER_TRADE:
        log_event("trade_spot", req.idempotency_key, req.model_dump(), "rejected", {"reason":"AMOUNT_OUT_OF_RANGE"})
        raise HTTPException(status_code=400, detail="Trade amount out of range")

    # TODO: implement real Binance calls
    result = {"accepted": True, "note": "stub; wire Binance later", "symbol": symbol, "side": req.side, "quote_amount": req.quote_amount}
    log_event("trade_spot", req.idempotency_key, req.model_dump(), "ok", result)
    return result

@app.post("/post")
def post(req: PostRequest):
    # TODO: implement real platform posting
    result = {"accepted": True, "note": "stub; wire platform APIs later", "platform": req.platform}
    log_event("post", req.idempotency_key, req.model_dump(), "ok", result)
    return result