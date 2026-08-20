from abc import ABC, abstractmethod

class NotificacionChannel(ABC):
    @abstractmethod
    def send(
        self,
        recipient: str,
        mensaje: str) -> None:
        pass
    
