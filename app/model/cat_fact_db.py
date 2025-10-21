import uuid
from sqlmodel import SQLModel, Field, Column
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy import String, func, DateTime, Boolean, text, JSON
from typing import Dict
import hashlib
from sqlalchemy.dialects.postgresql import JSONB

class Users(SQLModel, table=True):
    id: str = Field(
    default_factory=lambda: str(uuid.uuid4()),
    sa_column=Column(String(36), primary_key=True, nullable=False)
    )
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, nullable=False, index=True)
    )
    stack: str = Field(
        sa_column=Column(String, nullable=False))
    name: str = Field(
        sa_column=Column(String, nullable=False))
    role: str = Field(
        sa_column=Column(String, nullable=False, index=True))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False, server_default=text("true"), index=True))
    verify: bool = Field(default=False, sa_column=Column(Boolean, nullable=False, server_default=text("false"), index=True))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))


class StringAnalysis(SQLModel, table=True):
    id: str = Field(
        sa_column=Column(String(64), primary_key=True, nullable=False)
    )
    value: str = Field(
        sa_column=Column(String, unique=True, nullable=False)
    )
    # Properties as a nested JSON object
    properties: Dict = Field(
        sa_column=Column(JSONB, nullable=False)
    )
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    @classmethod
    def create_with_hash(cls, value: str):
        """Create a new instance with SHA-256 hash as ID and computed properties"""
        # Generate SHA-256 hash of the value
        hash_id = hashlib.sha256(value.encode('utf-8')).hexdigest()
        normalized = "".join(value.lower().split())
        is_palindrome = normalized == normalized[::-1]
        # Compute properties
        properties = {
            "length": len(value),
            "is_palindrome": is_palindrome,
            "unique_characters": len(set(value)),
            "word_count": len(value.split()),
            "sha256_hash": hash_id,
            "character_frequency_map": cls._get_character_frequency(value)
        }
        
        return cls(
            id=hash_id,
            value=value,
            properties=properties
        )
    @staticmethod
    def _get_character_frequency(text: str) -> Dict[str, int]:
        """Calculate character frequency map"""
        freq_map = {}
        for char in text:
            freq_map[char] = freq_map.get(char, 0) + 1
        return freq_map