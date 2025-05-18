from home.states.bet_states.manager_states import ManagerState
from home.states.bet_states.closed import Closed

class Matched(ManagerState):

    def matcher(self, bet):
        raise Exception("A entrada já foi correspondida")
        
    def closer(self, bet):
        bet.set_state(state=Closed())