from abc import ABC, abstractmethod


class ExtractInfoLadder(ABC):

    @abstractmethod
    def get_exposition_info(self, runner_id: str):
        pass