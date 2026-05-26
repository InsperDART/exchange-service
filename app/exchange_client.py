import httpx
import os
from fastapi import HTTPException, status

EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
EXCHANGERATE_BASE_URL = "https://v6.exchangerate-api.com/v6"

# Margem aplicada sobre a taxa base para calcular sell e buy.
# sell = rate * (1 + SPREAD)   → você vende moeda estrangeira mais caro
# buy  = rate * (1 - SPREAD)   → você compra moeda estrangeira mais barato
SPREAD = float(os.getenv("EXCHANGE_SPREAD"))


async def get_rate(from_currency: str, to_currency: str) -> dict:
    """
    Consulta a ExchangeRate-API e retorna sell, buy e date.
    Endpoint usado: GET /v6/{key}/pair/{from}/{to}
    """
    url = f"{EXCHANGERATE_BASE_URL}/{EXCHANGERATE_API_KEY}/pair/{from_currency.upper()}/{to_currency.upper()}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)

    if response.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Currency pair {from_currency}/{to_currency} not found",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch exchange rate from external API",
        )

    data = response.json()

    if data.get("result") != "success":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data.get("error-type", "Unknown error from exchange API"),
        )

    rate = data["conversion_rate"]
    # last_update_utc vem no formato "Thu, 22 May 2025 00:00:01 +0000"
    raw_date = data.get("time_last_update_utc", "")

    return {
        "sell": round(rate * (1 + SPREAD), 6),
        "buy":  round(rate * (1 - SPREAD), 6),
        "date": raw_date,
    }
