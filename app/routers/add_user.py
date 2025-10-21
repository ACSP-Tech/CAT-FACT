from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from ..schema.add_user import Register, MessageOut, Resend
from ..crud.add_user import user_register, verify_user, resend_email_verification
from ..database_setup import get_db

router = APIRouter(prefix="/user", tags=["Add User"])

@router.post("/signup", status_code=status.HTTP_202_ACCEPTED, response_model=MessageOut)
async def add_user(data:Register, backgroundtask:BackgroundTasks, session=Depends(get_db)):
    """
    step 1: user verification flow
    - add user route, create user, send verification email to user
    - Args: 
        - data: Register Input Schema, Body parameter
        - background_tasks: default FastAPI background tasks for sending email
    - raises:
        - HTTPException 500 for internal server error and 409 conflict for duplicate email
    - Returns:
        - MessageOut output schema, 202 Accepted
        - send verification email to client asynchronously
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
    

@router.get("/verify-email", status_code=status.HTTP_202_ACCEPTED, response_model=MessageOut)
async def email_verification(token: str, backgroundtask:BackgroundTasks, session=Depends(get_db)):
    """
    step 2: user verification flow
    - Verification route by users, verification can only occur once.
    - Args:
        - token: query paramenter from user verification url sent
        - takes no argument
        - raises: 400 Bad request for email already verified, 500 for internal server error
    - Returns:
        - MessageOut output schema, 202 created
        - send welcome email to client and client user_id to be used to display their random cat info
        - check inbox or spam folder for the email
    """
    try:
        return await verify_user(token, backgroundtask, session)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/resend-email", status_code=status.HTTP_202_ACCEPTED, response_model=MessageOut)
async def resend_email(data:Resend, backgroundtask:BackgroundTasks, session=Depends(get_db)):
    """
    step 3: user verification flow(should in case user did not receive verification email, or token expired)
    - resend email verification endpoint, frontend integration or use postman
    - Args: 
        - data: resend Input Schema, Body parameter
        - raises:
            - HTTPException 500 for internal server error and 400 bad request for already verified email
    - Returns:
        - MessageOut output schema, 201 created
        - send verification email to client
    """
    try:
        return await resend_email_verification(data, session, backgroundtask)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )