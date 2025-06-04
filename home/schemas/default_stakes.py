from pydantic import BaseModel, ConfigDict


class StakeDefaultSchema(BaseModel):
    stake: float

class StakeDefaultPublic(StakeDefaultSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)