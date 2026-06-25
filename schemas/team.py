from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from typing import Optional
from schemas.player import PlayerResponse


class TeamCreate(BaseModel):
    name: str
    code: str = Field(min_length=3, max_length=3)

    @field_validator("code", mode="before")
    @classmethod
    def normalize_code(cls, value):
        if not isinstance(value, str):
            raise ValueError("Code must be a string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Code cannot be empty")
        if len(stripped) != 3:
            raise ValueError("Code must have exactly 3 characters")
        return stripped.upper()

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Name cannot be empty")
        return stripped


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


class TeamResponse(BaseModel):
    id: int
    name: str
    code: str
    group_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeamWithPlayers(TeamResponse):
    players: list["PlayerResponse"] = []

    model_config = ConfigDict(from_attributes=True)


TeamWithPlayers.model_rebuild()
