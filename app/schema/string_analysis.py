from .general import StrictBaseModel as BaseModel
from pydantic import Field, field_validator
from typing import Annotated
from fastapi import HTTPException, status
from typing import Dict, List, Optional, Any
from datetime import datetime

class StringBody(BaseModel):
    value: Annotated[str, Field(description="string to analyze")]
    #custom validation for value
    @field_validator("value")
    def validate_value(cls, v: str) -> str:
        if not v:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request body or missing {v} field")
        v = v.strip() # Remove leading/trailing spaces e.g "  John Doe  " -> "John Doe"
        if not v:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid request body or missing {v} field")
        #Prevent consecutive spaces
        if "  " in v:  
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Value cannot contain consecutive spaces")
        #sentencase casing for insensitive match
        return v.lower()
    
class StringAnaly(BaseModel):
    id: str
    value: str 
    properties: Dict 
    created_at: datetime

class StringQuery(BaseModel):
    is_palindrome: Optional[bool] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    word_count: Optional[int] = None
    contains_character: Optional[str] = None

class StringFil(BaseModel):
    data: List[StringAnaly]
    count: int
    filters_applied: Dict[str, Any]

class StringInter(BaseModel):
    original: str
    parsed_filters: Dict[str, Any]

class StringNat(BaseModel):
    data: List[StringAnaly]
    count: int
    interpreted_query: StringInter