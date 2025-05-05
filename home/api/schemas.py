from ninja import Schema


class BetSchema(Schema):
    runner_id: str
    market_id: str
    event_id: str
    side: str
    odd: float
    stake: float

    def __repr__(self):
        return f'[{self.event_id}][{self.market_id}][{self.runner_id}][{self.odd}][{self.stake}][{self.side}]'


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
