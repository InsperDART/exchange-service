from fastapi import Header, HTTPException, status
import jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET", "secret")
ALGORITHM  = os.getenv("JWT_ALGORITHM", "HS256")


def verify_token(authorization: str = Header(...)) -> dict:
    """
    Valida o Bearer JWT enviado pelo gateway.
    Retorna o payload do token (contém o id-account / sub).
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with 'Bearer '",
        )

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
