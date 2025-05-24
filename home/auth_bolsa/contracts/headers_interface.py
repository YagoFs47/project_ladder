from abc import ABC, abstractmethod


class HeadersInterface(ABC):

    @abstractmethod
    def load_headers_bolsa(self) -> dict:
        pass

    @abstractmethod
    def load_headers_exchange(self) -> dict:
        pass
