from abc import ABC, abstractmethod


class ManagerState(ABC):

    @abstractmethod
    def matcher(self) -> None:
        pass

    @abstractmethod
    def closer(self) -> None:
        pass
