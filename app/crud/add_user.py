from ..model.cat_fact_db import Users
from fastapi import HTTPException, status
from sqlmodel import select, func
from ..utils.add_user import encode_email_token, send_verification_email
from ..schema.add_user import MessageOut

async def user_register(data, session, backgroundtask):
    try:
        #avoid duplicate
        statement = select(Users).where(Users.email == data.email)
        result = await session.execute(statement)
        user_email = result.scalars().first()
        if user_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {data.email} already registered"
            )
        # role auto seeding
        statement_role = select(func.count()).select_from(Users)
        result = await session.execute(statement_role)
        user_role = result.scalar_one()
        user_role = "superadmin" if user_role == 0 else "user"
        #add user
        new_user = Users(
            email = data.email,
            name = data.name,
            stack = data.stack,
            role = user_role
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        first_name = data.name.split()[0] if data.name and data.name.strip() else data.name
        payload = {
            "email": data.email,
            "first_name": first_name,
            "type": "email_verification"
        }
        email_token = await encode_email_token(payload)
        backgroundtask.add_task(
            send_verification_email,
            email=data.email,
            token=email_token,
            username=data.first_name
        )
        response = f"Account successfully registered, Kindly check {data.email} inbox or spam folder to verify your account"
        return MessageOut(message=response)
    except HTTPException as Httpexc:
        await session.rollback()
        raise Httpexc
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register user: {str(e)}"
        )  