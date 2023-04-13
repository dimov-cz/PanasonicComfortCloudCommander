from typing import Optional
from .RequestType import RequestType
from .PccAccount import PccAccount
from .ACDevice import ACDevice
class Request:
    type: RequestType
    account: Optional[PccAccount]
    device: Optional[ACDevice]
    data = None
    
    def __init__(self, type: RequestType, account: Optional[PccAccount] = None, device: Optional[ACDevice] = None, data = None) -> None:
        self.type = type
        self.account = account
        self.device = device
        self.data = data
        
    def __str__(self) -> str:
        return f"Request(type={self.type}, account={self.account}, device={self.device}, data={self.data})"