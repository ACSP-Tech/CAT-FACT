from .general import StrictBaseModel as BaseModel
from pydantic import EmailStr, Field, field_validator
from typing import Annotated
import re

class Register(BaseModel):
    email: EmailStr
    stack: Annotated[str, Field(min_length=3, max_length=50, description="Backend technology stack in format 'Language/Framework' (e.g., 'Python/FastAPI', 'Node.js/Express', 'Go/Gin')")]
    name: Annotated[str,Field(
            min_length=7,
            max_length=50,
            description="Full name must be 7 to 50 characters long, only letters, two spaces, and at most one hyphen"
        )
    ]
    #custom validation for full_name
    @field_validator("name")
    def validate_full_name(cls, v: str) -> str:
        v = v.strip() # Remove leading/trailing spaces e.g "  John Doe  " -> "John Doe"
        # Ensure only letters, spaces, and hyphen are present
        if not re.fullmatch(r"[A-Za-z\s-]+", v):
            raise ValueError("Full name may only contain letters, spaces, and hyphen")
        #Prevent consecutive spaces
        if "  " in v:  
            raise ValueError("Full name must not contain consecutive spaces")
        # Ensure at least one space and at most two spaces
        if v.count(" ") < 1:
            raise ValueError("Full name must contain at least one space")
        if v.count(" ") > 2:
            raise ValueError("Full name must contain at most 2 spaces")
        #Hyphen not allowed at start or end
        if v.startswith("-") or v.endswith("-"):
            raise ValueError("Full name cannot start or end with a hyphen")
        # Ensure at most one hyphen
        if v.count("-") > 1:
            raise ValueError("Full name must contain at most one hyphen")
        #Hyphen not allowed at start or end
        return v.title()
    #remove trailing space and make email lowercase
    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()
    #custom validator for stck
    @field_validator("stack")
    def validate_stack(cls, v: str) -> str:
        v = v.strip()
        
        # Pattern: Language/Framework (e.g., "Python/Django", "Node.js/Express")
        pattern = r"^[A-Za-z\.\#\+]+/[A-Za-z\.\#]+$"
        
        if not re.match(pattern, v):
            raise ValueError(
                "Stack must be in format 'Language/Framework' (e.g., 'Python/FastAPI', 'Node.js/Express')"
            )
        
        # Ensure minimum length for both parts
        parts = v.split("/")
        if len(parts[0]) < 2 or len(parts[1]) < 2:
            raise ValueError("Both language and framework must be at least 2 characters")

        return v.title()
    
class MessageOut(BaseModel):
    message: str
    