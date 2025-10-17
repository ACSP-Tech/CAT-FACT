import uuid
from sqlmodel import SQLModel, Field, Column
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy import String, func, DateTime, Integer, desc, Index, Boolean, text

class Users(SQLModel, table=True):
    id: str = Field(
    default_factory=lambda: str(uuid.uuid4()),
    sa_column=Column(String(36), primary_key=True, nullable=False)
    )
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, nullable=False, index=True)
    )
    hashed_password: str = Field(
        sa_column=Column(String, nullable=False))
    name: str = Field(
        sa_column=Column(String, nullable=False))
    role: str = Field(
        sa_column=Column(String, nullable=False, index=True))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False, server_default=text("true"), index=True))
    verify: bool = Field(default=False, sa_column=Column(Boolean, nullable=False, server_default=text("false"), index=True))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    