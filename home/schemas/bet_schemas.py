from datetime import datetime

from pydantic import BaseModel, Field


class BetSchema(BaseModel):
    bet_id: str = Field(validation_alias="id")
    event_id: str = Field(validation_alias="event-id")
    market_id: str = Field(validation_alias="market-id")
    runner_id: str = Field(validation_alias="runner-id")
    odd: float = Field(
        validation_alias="odds", 
        serialization_alias="odd")
    side: str
    stake: float
    stake_matched: str = Field(validation_alias="stake-matched")
    status: str
    created_at: datetime = Field(validation_alias="created-at")


class BetPayloadSchema(BaseModel):
    runner_id: str = Field(serialization_alias="runner-id")
    market_id: str = Field(serialization_alias="market-id")
    event_id: str = Field(serialization_alias="event-id")
    side: str
    odd: float = Field(serialization_alias="odds")
    stake: float
    status: str
    keep_in_play: bool = Field(
        serialization_alias="keep-in-play",
        default=True)
