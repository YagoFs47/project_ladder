from ninja import Schema


class BetSchema(Schema):
    runner_id: str
    market_id: str
    event_id: str
    side: str
    odds: float
    stake: float
    keep_in_play: bool

    def __repr__(self):
        return f'[{self.event_id}][{self.market_id}][{self.runner_id}][{self.odd}][{self.stake}][{self.side}]'

    def to_json(self):
        return {
            "runner-id": self.runner_id,
            "market-id": self.market_id,
            "event-id": self.event_id,
            "keep-in-play": self.keep_in_play,
            "side": self.side,
            "odds": self.odds,
            "stake": self.stake
        }

class BetSchemaPubli(Schema):
    pk: int
    runner_id: str
    market_id: str
    event_id: str
    side: str
    odd: float
    stake: float
    is_finished: bool
    status: bool
