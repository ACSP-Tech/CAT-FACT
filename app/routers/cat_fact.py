from fastapi import APIRouter, HTTPException, status, Depends
from ..crud.cat_fact import get_me, get_user
from ..database_setup import get_db
from ..schema.cat_fact import MeOut

router = APIRouter(tags=["Add User"])

@router.get("/me", status_code=status.HTTP_200_OK, response_model=MeOut)
async def fetch_me(session=Depends(get_db)):
    """
    endpoint to fetch my info with random cat fact
    - Args: take no argument
    - returns 200 
    """
    try:
        return await get_me(session)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/user", status_code=status.HTTP_200_OK, response_model=MeOut)
async def fetch_user(q: str, session=Depends(get_db)):
    """
    endpoint to fetch user info with random cat fact
    - Args: take no argument
    - returns 200 
    """
    try:
        return await get_user(q, session)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )