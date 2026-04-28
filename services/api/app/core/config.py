import os
from functools import lru_cache
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Settings(BaseModel):
    environment: str = Field(default="development")
    storage_backend: str = Field(default="memory")
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    payment_provider: str = Field(default="mock")
    report_price_inr: int = Field(default=1499)
    supabase_url: str = Field(default="")
    supabase_service_role_key: str = Field(default="")
    razorpay_key_id: str = Field(default="")
    razorpay_key_secret: str = Field(default="")
    razorpay_webhook_secret: str = Field(default="")
    google_maps_api_key: str = Field(default="")
    mappls_rest_api_key: str = Field(default="")
    here_api_key: str = Field(default="")

    @classmethod
    def from_env(cls) -> "Settings":
        _load_env_files()
        origins = os.getenv(
            "LOCATIONIQ_CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        )
        razorpay_key_id = os.getenv("RAZORPAY_KEY_ID") or os.getenv(
            "NEXT_PUBLIC_RAZORPAY_KEY_ID",
            "",
        )
        razorpay_key_secret = os.getenv("RAZORPAY_KEY_SECRET", "")
        payment_provider = os.getenv("LOCATIONIQ_PAYMENT_PROVIDER")
        if payment_provider is None:
            payment_provider = "razorpay" if razorpay_key_id and razorpay_key_secret else "mock"

        return cls(
            environment=os.getenv("LOCATIONIQ_ENV", "development"),
            storage_backend=os.getenv("LOCATIONIQ_STORAGE", "memory"),
            cors_origins=[origin.strip() for origin in origins.split(",") if origin.strip()],
            payment_provider=payment_provider,
            report_price_inr=int(os.getenv("LOCATIONIQ_REPORT_PRICE_INR", "1499")),
            supabase_url=os.getenv("SUPABASE_URL", ""),
            supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
            razorpay_key_id=razorpay_key_id,
            razorpay_key_secret=razorpay_key_secret,
            razorpay_webhook_secret=os.getenv("RAZORPAY_WEBHOOK_SECRET", ""),
            google_maps_api_key=os.getenv("GOOGLE_MAPS_API_KEY", ""),
            mappls_rest_api_key=os.getenv("MAPPLS_REST_API_KEY")
            or os.getenv("MAPPLS_API_KEY", ""),
            here_api_key=os.getenv("HERE_API_KEY", ""),
        )


def _load_env_files() -> None:
    root = Path(__file__).resolve().parents[4]
    for env_file in (root / ".env.local", root / ".env"):
        if env_file.exists():
            load_dotenv(env_file, override=False)


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
