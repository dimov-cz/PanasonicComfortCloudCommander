from typing import Optional
from enum import Enum
import json

from .ACDeviceStateValue import ACDeviceStateValue

class ACDeviceState:
    temperatureInside: Optional[float] = None
    temperatureOutside: Optional[float] = None
    temperature: Optional[float] = None
    power: Optional[ACDeviceStateValue] = None
    mode: Optional[ACDeviceStateValue] = None
    fanSpeed: Optional[ACDeviceStateValue] = None
    airSwingHorizontal: Optional[ACDeviceStateValue] = None
    airSwingVertical: Optional[ACDeviceStateValue] = None
    eco: Optional[ACDeviceStateValue] = None
    nanoe: Optional[ACDeviceStateValue] = None
    
    def __init__(self) -> None:
        pass
    
    def __str__(self) -> str:
        return f"ACDeviceState(temperatureInside={self.temperatureInside}, temperatureOutside={self.temperatureOutside}, temperature={self.temperature}, power={self.power}, mode={self.mode}, fanSpeed={self.fanSpeed}, airSwingHorizontal={self.airSwingHorizontal}, airSwingVertical={self.airSwingVertical}, eco={self.eco}, nanoe={self.nanoe})"
    
    def normalize(self):
        if not self.power is None and not isinstance(self.power, ACDeviceStateValue):
            self.power = ACDeviceStateValue(int(self.power))
        if not self.mode is None and not isinstance(self.mode, ACDeviceStateValue):
            self.mode = ACDeviceStateValue(int(self.mode))
        if not self.temperature is None and not isinstance(self.temperature, float):
            self.temperature = float(self.temperature)
        
    
    @staticmethod
    def pccConstToData(obj):
        if issubclass(obj.__class__, Enum):
            return ACDeviceStateValue(obj.value, obj.name)
        return super().default(obj)      
    
    @staticmethod
    def createFromPcc(data):
        data = data["parameters"]
        obj = ACDeviceState()
        obj.temperatureInside = data["temperatureInside"]
        obj.temperatureOutside = data["temperatureOutside"]
        obj.temperature = data["temperature"]
        obj.power = ACDeviceState.pccConstToData(data["power"])
        obj.mode = ACDeviceState.pccConstToData(data["mode"])
        obj.fanSpeed = ACDeviceState.pccConstToData(data["fanSpeed"])
        obj.airSwingHorizontal = ACDeviceState.pccConstToData(data["airSwingHorizontal"])
        obj.airSwingVertical = ACDeviceState.pccConstToData(data["airSwingVertical"])
        obj.eco = ACDeviceState.pccConstToData(data["eco"])
        obj.nanoe = ACDeviceState.pccConstToData(data["nanoe"])
        return obj
    
    def __json__(self):
        json.dumps(self, cls=ACDeviceStateEncoder)

""" @interal 
"""
class ACDeviceStateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ACDeviceState):
            return {
                "temperatureInside": obj.temperatureInside,
                "temperatureOutside": obj.temperatureOutside,
                "temperature": obj.temperature,
                "power": obj.power,
                "mode": obj.mode,
                "fanSpeed": obj.fanSpeed,
                "airSwingHorizontal": obj.airSwingHorizontal,
                "airSwingVertical": obj.airSwingVertical,
                "eco": obj.eco,
                "nanoe": obj.nanoe
            }
        if isinstance(obj, ACDeviceStateValue):
            return {
                "value": obj.value,
                "strValue": obj.strValue
            }
        return super().default(obj)