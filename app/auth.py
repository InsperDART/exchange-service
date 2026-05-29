from fastapi import Header, HTTPException, status

def verify_token(
    id_account: str = Header(..., alias="id-account")
) -> dict:
    if not id_account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing id-account header",
        )
    return {"sub": id_account}