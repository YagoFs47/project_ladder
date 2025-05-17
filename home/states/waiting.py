from home.states.manager_states import ManagerState
from home.states.matched import Matched

class Waiting(ManagerState):
    
    def matcher(self, bet):
        bet.set_state(state=Matched())
        
    def closer(self, bet):
        raise Exception("A entrada ainda não foi correspondida")