from decimal import Decimal
from .core.config import config
from datetime import datetime, UTC
from sqlmodel import Field, SQLModel
import sqlalchemy as sa


# base model for all models
# makes sure that all models are created in the appropriate schema
class BaseModel(SQLModel):
    __table_args__ = {"schema": str(config.DB_SCHEMA)}


class CreateReport(BaseModel):
    accommodation_id: int

class CreateReportFull(CreateReport):
    user_id: int


class Report(BaseModel, table=True):
    id: int = Field(primary_key=True, default=None)

    user_id: int
    accommodation_id: int

class ReportsPublic(BaseModel):
    data: list[Report]


class CreateReportPublic(BaseModel):
    id: int
    msg: str
