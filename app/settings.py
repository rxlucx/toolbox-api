from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # IMPORTANT: these must be set via env vars in Hostinger / compose
    BINANCE_API_KEY: str = ""
    BINANCE_API_SECRET: str = ""
    X_BEARER_TOKEN: str = ""          # or OAuth tokens later
    NOTION_TOKEN: str = ""
    NOTION_DATABASE_ID: str = ""
    PINTEREST_TOKEN: str = ""
    GUMROAD_TOKEN: str = ""

    # Guardrails
    TRADING_ENABLED: bool = False
    MAX_USDT_PER_TRADE: float = 25.0
    DAILY_LOSS_CAP_USDT: float = 50.0
    SYMBOL_ALLOWLIST: str = "BTCUSDT,ETHUSDT"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()