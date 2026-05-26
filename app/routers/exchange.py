from fastapi import APIRouter, Depends
from app.auth import verify_token
from app.exchange_client import get_rate
from app.schemas import ExchangeResponse

router = APIRouter(prefix="/exchanges", tags=["exchange"])


@router.get("/{from_currency}/{to_currency}", response_model=ExchangeResponse)
async def exchange_rate(
    from_currency: str,
    to_currency: str,
    token_payload: dict = Depends(verify_token),
):
    """
    Retorna a taxa de câmbio entre duas moedas.
    Requer autenticação via Bearer JWT.

    Exemplo: GET /exchanges/USD/EUR
    """

    id_account = token_payload.get("sub") or token_payload.get("id") or token_payload.get("account_id", "")

    rate_data = await get_rate(from_currency, to_currency)

    return ExchangeResponse(**{
        "sell":       rate_data["sell"],
        "buy":        rate_data["buy"],
        "date":       rate_data["date"],
        "id-account": str(id_account),
    })
