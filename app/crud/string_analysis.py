from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.string_analysis import StringFil, StringQuery, StringNat, StringAnaly
from ..model.cat_fact_db import StringAnalysis
from sqlmodel import select, and_, func, cast, Integer, Boolean, String
from sqlalchemy.orm import defer
from ..utils.string_analysis import interpret_natural_language_query
from fastapi_pagination.ext.sqlalchemy import paginate

async def get_current_string(val, session):
    try:
        vals = val.strip().lower()
        statement = select(StringAnalysis).options(defer(StringAnalysis.updated_at)).where(StringAnalysis.value == vals)
        result = await session.execute(statement)
        old_string = result.scalars().first()
        if not old_string:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="string does not exist in the system"
            )
        return old_string 
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise e
    


async def create_single_string(val, session):
    try:
        stmt = select(StringAnalysis).where(StringAnalysis.value == val.value)
        result = await session.execute(stmt)
        old_string = result.scalars().first()
        if old_string:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="String already exists in the system"
            )
        new_string = StringAnalysis.create_with_hash(val.value) 
        session.add(new_string)
        await session.commit()
        await session.refresh(new_string)
        return await get_current_string(val.value, session)
    except HTTPException as httpexc:
        await session.rollback()
        raise httpexc
    except Exception as e:
        await session.rollback()
        raise e
    
async def all_single_string(params, session):
    try:
        stmt = select(StringAnalysis).options(defer(StringAnalysis.updated_at)).order_by(StringAnalysis.created_at.desc())
        return await paginate(session, stmt, params)
    except HTTPException as httpexc:
        await session.rollback()
        raise httpexc
    except Exception as e:
        await session.rollback()
        raise e
    
async def delete_single_string(string_value, session):
    try:
        vals = string_value.strip().lower()
        statement = select(StringAnalysis).options(defer(StringAnalysis.updated_at)).where(StringAnalysis.value == vals)
        result = await session.execute(statement)
        old_string = result.scalars().first()
        if not old_string:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="string does not exist in the system"
            )
        await session.delete(old_string)
        await session.commit()
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise e

        
async def all_string_fil(is_palindrome, min_length, max_length, word_count, contains_character, session):
    try:
        filters = []
        # Filter by palindrome if specified
        if is_palindrome is not None:
            filters.append(cast(StringAnalysis.properties["is_palindrome"], Boolean) == is_palindrome)
        # Filter by min_length if specified
        if min_length is not None:
            filters.append(cast(StringAnalysis.properties["length"], Integer) >= min_length)
        # Filter by max_length if specified
        if max_length is not None:
            filters.append(cast(StringAnalysis.properties["length"], Integer) <= max_length)
        # Filter by max_length if specified
        if word_count is not None:
            filters.append(cast(StringAnalysis.properties["word_count"], Integer) == word_count)
        #filter by contains_character if specified
        if contains_character is not None:
            filters.append(StringAnalysis.value.ilike(f"%{contains_character}%"))
        if not filters:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Invalid query parameter values or types"
            )
        #select matching fields
        statement = select(StringAnalysis).options(defer(StringAnalysis.updated_at)).where(and_(*filters))
        result = await session.execute(statement)
        old_strings = result.scalars().all()

        stmt = select(func.count()).select_from(StringAnalysis).where(and_(*filters))
        count_result = await session.execute(stmt)
        result_count = count_result.scalar()

        fil = StringQuery(
            is_palindrome = is_palindrome,
            min_length = min_length,
            max_length = max_length,
            word_count = word_count,
            contains_character = contains_character
        )

        filstring = [
            StringAnaly(
                id=s.id,
                value=s.value,
                properties=s.properties,
                created_at=s.created_at
            )
            for s in old_strings
        ]

        filtered_result = StringFil(
            data = filstring,
            count = result_count,
            filters_applied = fil.model_dump(exclude_none=True) #{k: v for k, v in fil.model_dump().items() if v is not None}
        )
        return filtered_result
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise e

async def natural_language_filtering(query, session):
    try:
        parsed_filters = await interpret_natural_language_query(query)
        if not parsed_filters:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail= "Unable to parse natural language query"
                )
        result = await all_string_fil(
                is_palindrome=parsed_filters.get("is_palindrome"),
                min_length=parsed_filters.get("min_length"),
                max_length=parsed_filters.get("max_length"),
                word_count=parsed_filters.get("word_count"),
                contains_character=parsed_filters.get("contains_character"),
                session=session
            )
        return StringNat(
                data = result.data,
                count = result.count,
                interpreted_query = {
                    "original": query,
                    "parsed_filters": result.filters_applied
                })
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise e