from ..model.cat_fact_db import Users
from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlmodel import select
from schema.cat_fact import MeOut, MeUser
from datetime import datetime, timezone
from ..utils.cat_fact import fetch_cat_fact

async def get_me(session):
    try:
        # Fetch superadmin(me) user from database
        statement = select(Users).where(Users.role == "superadmin")
        result = await session.execute(statement)
        me = result.scalar_one()

        # Generate timestamp
        time = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

        # Fetch cat fact with error handling
        cat_fact = await fetch_cat_fact()
        
        # Build user response object
        me_res = MeUser(
            email = me.email,
            name = me.name,
            stack = me.stack
        )

        return MeOut(
            status ="success",
            user = me_res,
            timestamp = time,
            fact = cat_fact
        )

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Superadmin user not found"
        )
    except MultipleResultsFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data integrity error: Multiple superadmin users found"
        )
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving superadmin user"
        )
    
async def get_user(q, session):
    try:
        # Fetch user from database either with their userid 
        statement = select(Users).where(Users.id == q)
        result = await session.execute(statement)
        me = result.scalar_one()

        # Generate timestamp
        time = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

        # Fetch cat fact with error handling
        cat_fact = await fetch_cat_fact()
        
        # Build user response object
        me_res = MeUser(
            email = me.email,
            name = me.name,
            stack = me.stack
        )

        return MeOut(
            status ="success",
            user = me_res,
            timestamp = time,
            fact = cat_fact
        )

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Superadmin user not found"
        )
    except MultipleResultsFound:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Data integrity error: Multiple superadmin users found"
        )
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving superadmin user"
        )