"""
    strValue is not mandatory/reliable, it's used only for real-time updates from PCC
"""
from typing import Optional


class ACDeviceStateValue:
    strValue: str
    
    def __init__(self, value, strValue: Optional[str] = None) -> None:
        self.value = value
        self.strValue = strValue if not strValue is None else str(value)
        
    def __str__(self) -> str:
        return str(self.strValue) + "(" + str(self.value) + ")"
    
    def matches(self, test) -> bool:
        if self.value is None: return True
        if test is None: return False
        if hasattr(test, "value"):
            return self.value == test.value
        return self.value == test