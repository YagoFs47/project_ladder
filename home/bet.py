"""
Esse módulo visa criar uma abstração OOP de uma aposta na Bolsa de Apostas
para faciliar as operações diversas contidas nas análises e ações e modificações de estados,
essa classe irá receber os dados da aposta criada na Bolsa, e também irá receber a instância
da aposta do nosso banco de dados, ou seja, uma instância de Open
"""
from typing import Union
from home.states.bet_states.waiting import Waiting
from home.states.bet_states.closed import Closed
from home.states.bet_states.matched import Matched


class Bet:
    
    WAITING = "waiting"
    MATCHED = "matched"
    CLOSED = "closed"

    _bet_id: str
    _event_id: str
    _market_id: str
    _runner_id: str
    _stake: float
    _stake_matched: float
    _event_name: str
    _odd: float
    _status: Union[Waiting, Closed, Matched] = Waiting()
    _side: str #[back | lay]

    def __init__(self, data: dict):
        self._bet_id = data.get('id')
        self._event_id = data.get("event-id")
        self._market_id = data.get("market-id")
        self._runner_id = data.get("runner-id")
        self._stake = data.get('stake')
        self._stake_matched = data.get('stake-matched')
        self._event_name = data.get('event-name')
        self._odd = data.get('odds')
        self._side = data.get("side")
    
    def get_status(self) -> str:
        """retorna o status da aposta"""
        return self._status
    
    def is_matched(self) -> bool:
        """retorna se a aposta foi correspondida ou não"""
        return self.get_status() == Matched()

    def get_market_id(self) -> str:
        """retorna o id do mercado"""
        return self._market_id

    def get_event_id(self) -> str:
        """retorna o id do evento"""
        return self._event_id
    
    def get_runner_id(self) -> str:
        """retorna o id do runner que variam entre OVER ou UNDER"""
        return self._runner_id

    def get_side(self) -> str:
        """retorna o lado que varia entre 'Back' or 'Lay'"""
        return self._side
    
    def set_state(self, state):
        """Change a state"""
        self._status = state
    
    def macher(self):
        """Change state of self.instance to Matched"""
        self._status.matcher()

    def closer(self):
        """Change state of self.instance to Closed"""
        self._status.closer()
    
    def save_bet(self):
        pass

    @classmethod
    def state_obj_to_str(state: Union[Waiting, Matched, Closed]):
        hash_states = {
            Waiting: "waiting",
            Matched: "matched",
            Closed: "closed"
        }
        if hash_states.get(state):
            return hash_states.get(state)
        
        raise Exception("Esse estado não existe")
    
    def state_str_to_obj(self, state: str) -> None:
        hash_states = {
            "waiting": Waiting,
            "matched": Matched,
            "closed": Closed
        }
        if hash_states.get(state):
            self._status = hash_states.get(state)()
        
        raise Exception("Esse estado não existe")