from ..model.cat_fact_db import Users
from fastapi import HTTPException, status
from sqlmodel import select, func, and_
from ..utils.add_user import encode_email_token, send_verification_email, decode_token, send_welcome_email
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
            "name": data.name,
            "type": "email_verification"
        }
        email_token = await encode_email_token(payload)
        backgroundtask.add_task(
            send_verification_email,
            email=data.email,
            token=email_token,
            username=first_name
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

async def verify_user(token, backgroundtask, session):
    try:
        payload = await decode_token(token)
        user_type = payload.get("type")
        user_name = payload.get("name")
        email = payload.get("email")
        #security setup, misleading response
        if user_type != "email_verification":
            response = "Email verified successfully! you Check your mail for the next steps."
            return MessageOut(
                message=response
            )
        statement = select(Users).where(and_(Users.email == email, Users.name == user_name))
        result = await session.execute(statement)
        user = result.scalars().first()
        #security setup
        if not user:
            raise HTTPException(
                status_code=status.HTTP_202_ACCEPTED,
                detail= "Email verified successfully! you can Check your mail for the next steps."
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user, contact support"
            )
        if user.verify:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )
        first_name = user.name.split()[0] if user.name and user.name.strip() else user.name
        # verify user
        user.verify = True
        # save to db
        await session.commit()
        await session.refresh(user)
        
        # send welcome email
        backgroundtask.add_task(
            send_welcome_email,
            email=user.email,
            username=first_name,
            user_id=user.id
        )
        response = "Email verified successfully! Check your mail for the next steps."
        return MessageOut(
            message=response
        )
    except HTTPException as Httpexc:
        await session.rollback()
        raise Httpexc
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed: {str(e)}"
        )

async def resend_email_verification(data, session, backgroundtask):
    try:
        #check if user exist
        statement = select(Users).where(Users.email == data.email)
        result = await session.execute(statement)
        user = result.scalars().first()
        #security setup
        if not user:
            response = f"Verification email resent, Kindly check {data.email} inbox or spam folder to verify your account"
            return MessageOut(message=response)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user, contact support"
            )
        if user.verify:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your account is already verified"
            )
        first_name = user.name.split()[0] if user.name and user.name.strip() else user.name
        payload = {
            "email": user.email,
            "name": user.name,
            "type": "email_verification"
        }
        email_token = await encode_email_token(payload)
        backgroundtask.add_task(
            send_verification_email,
            email=user.email,
            token=email_token,
            username=first_name
        )
        response = f"Verification email resent, Kindly check {data.email} inbox or spam folder to verify your account"
        return MessageOut(message=response)
    except HTTPException as Httpexc:
        session.rollback()
        raise Httpexc
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed: {str(e)}"
        )  