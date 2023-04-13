"""
    strValue is not mandatory/reliable, it's used only for real-time updates from PCC
"""
class ACDeviceStateValue:
    def __init__(self, value, strValue = None) -> None:
        self.value = value
        self.strValue = strValue
        
    def __str__(self) -> str:
        return str(self.strValue) + "(" + str(self.value) + ")"