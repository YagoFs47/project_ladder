from home.states.bet_states.manager_states import ManagerState


class Closed(ManagerState):

    def matcher(self, bet):
        raise Exception("A entrada já foi correspondida")

    def closer(self, bet):
        raise Exception("A entrada já foi fechada")
