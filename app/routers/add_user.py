from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from ..schema.add_user import Register, MessageOut
from ..crud.add_user import user_register
from ..database_setup import get_db

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/signup", status_code=status.HTTP_202_ACCEPTED, response_model=MessageOut)
async def register(data:Register, backgroundtask:BackgroundTasks, session=Depends(get_db)):
    """
    step 1: user verification flow
    add user route, create user, send verification email to user
    Args: 
        data: Register Input Schema, Body parameter
        background_tasks: default FastAPI background tasks for sending email
        raises:
            HTTPException 500 for internal server error and 409 conflict for duplicate email
    Returns:
        MessageOut output schema, 202 Accepted
        send verification email to client asynchronously
    """
    try:
        return await user_register(data, session, backgroundtask)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )