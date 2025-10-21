from fastapi import APIRouter, HTTPException, status, Depends, Query
from ..crud.string_analysis import create_single_string, get_current_string, all_single_string, delete_single_string, all_string_fil, natural_language_filtering
from ..database_setup import get_db
from ..schema.string_analysis import StringAnaly, StringBody, StringFil, StringNat
from typing import Optional
from fastapi_pagination import Page
from ..utils.string_analysis import StringParams

router = APIRouter(tags=["String Analysis"])

@router.post("/strings", status_code=status.HTTP_201_CREATED, response_model=StringAnaly)
async def create_string(value:StringBody, session=Depends(get_db)):
    """
    API to Create and Analyze String
    - Agrs:
        - value as body parameter
    -Return
        - Success Response (201 Created):
    - Error Response:
        - 409 Conflict: String already exists in the system
        - 400 Bad Request: Invalid request body or missing "value" field
        - 422 Unprocessable Entity: Invalid data type for "value" (must be string)

    """
    try:
        return await create_single_string(value, session)
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/strings/filter-by-natural-language", response_model=StringNat, status_code=status.HTTP_200_OK)
async def natural_language_filtering_endpoint(
    query: Optional[str] = Query(None, description="user text to string"),
    session = Depends(get_db)):
    """
    Endpoint to filter by user text
    - Args:
        - takes 1 query paramter as string
    """
    try:
        return await natural_language_filtering(query, session)
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.get("/strings/{string_value}", status_code=status.HTTP_200_OK, response_model=StringAnaly)
async def single_current_string(string_value:str, session=Depends(get_db)):
    """
    API to Create and Analyze String
    - Agrs:
        - value as body parameter
    -Return
        - Success Response (201 Created):
    - Error Response:
        - 409 Conflict: String already exists in the system
        - 400 Bad Request: Invalid request body or missing "value" field
        - 422 Unprocessable Entity: Invalid data type for "value" (must be string)

    """
    try:
        return await get_current_string(string_value, session)
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/strings/search/all", response_model=Page[StringAnaly], status_code = status.HTTP_200_OK)
async def all_strings(params: StringParams = Depends(), session = Depends(get_db)):
    """
    API to Create and Analyze String
    - Agrs:
        - value as body parameter
    -Return
        - Success Response (201 Created):
    - Error Response:
        - 409 Conflict: String already exists in the system
        - 400 Bad Request: Invalid request body or missing "value" field
        - 422 Unprocessable Entity: Invalid data type for "value" (must be string)

    """
    try:
        return await all_single_string(params, session)
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
@router.delete("/strings/{string_value}", status_code=status.HTTP_204_NO_CONTENT)
async def single_string_delete_endpoint(string_value:str, session=Depends(get_db)):
    """
    API to Create and Analyze String
    - Agrs:
        - value as body parameter
    -Return
        - Success Response (201 Created):
    - Error Response:
        - 409 Conflict: String already exists in the system
        - 400 Bad Request: Invalid request body or missing "value" field
        - 422 Unprocessable Entity: Invalid data type for "value" (must be string)

    """
    try:
        response = await delete_single_string(string_value, session)
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.get("/strings", response_model=StringFil, status_code=status.HTTP_200_OK)
async def all_strings_fil_endpoint(
    is_palindrome: Optional[bool] = Query(None, description="Filter by palindrome status"),
    min_length: Optional[int] = Query(None, description="Minimum string length"), 
    max_length: Optional[int] = Query(None, description="Maximum string length"),
    word_count: Optional[int] = Query(None, description="Exact word count"),
    contains_character: Optional[str] = Query(None, description="Character or substring to search for"),
    session = Depends(get_db)):
    """
    Endpoint to get all strings with filtering
    - Args:
        - takes 5 query parameters
    """
    try:
        return await all_string_fil(is_palindrome, min_length, max_length, word_count, contains_character, session)
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

