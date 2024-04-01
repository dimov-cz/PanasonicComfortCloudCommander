from typing import Any, Optional
from .ACDevice import ACDevice
from .ResponseType import ResponseType

class Response:
    
    device: Optional[ACDevice]
    type: ResponseType
    data: Optional[dict]
    
    def __init__(self, type: ResponseType, device: Optional[ACDevice] = None, data: Any = None) -> None:
        self.device = device
        self.type = type
        self.data = data
    def __str__(self) -> str:
        return f"Response(acDevice={self.device}, type={self.type}, data={self.data})"

