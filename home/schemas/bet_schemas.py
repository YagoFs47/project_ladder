from datetime import datetime
from colorama import init, Fore
from pydantic import BaseModel, Field
init()

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
    liquidity: float = Field(default=0)
    stake_matched: float = Field(validation_alias="stake-matched")
    partial_stake: float
    status: str
    created_at: datetime = Field(validation_alias="created-at")

    def __str__(self):
        return f'STK={Fore.BLUE}{self.stake}{Fore.RESET} | PSTK={Fore.MAGENTA}{self.partial_stake}{Fore.RESET} | ODD={Fore.YELLOW}{self.odd}{Fore.RESET} | STATUS={Fore.LIGHTCYAN_EX}{self.status}{Fore.RESET} | SIDE={Fore.LIGHTGREEN_EX}{self.side}{Fore.RESET}'


class BetPayloadSchema(BaseModel):
    runner_id: str = Field(serialization_alias="runner-id")
    market_id: str = Field(serialization_alias="market-id")
    event_id: str = Field(serialization_alias="event-id")
    side: str
    odd: float = Field(serialization_alias="odds")
    stake: float
    status: str = Field(default="open")
    keep_in_play: bool = Field(
        serialization_alias="keep-in-play",
        default=True)
