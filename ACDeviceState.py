from typing import Optional
from enum import Enum
import json

from .ACDeviceStateValue import ACDeviceStateValue

class ACDeviceState:
    available: Optional[bool] = None
    temperatureInside: Optional[float] = None
    temperatureOutside: Optional[float] = None
    temperature: Optional[float] = None
    power: Optional[ACDeviceStateValue] = None
    mode: Optional[ACDeviceStateValue] = None
    presetId: Optional[str] = None
    fanSpeed: Optional[ACDeviceStateValue] = None
    airSwingHorizontal: Optional[ACDeviceStateValue] = None
    airSwingVertical: Optional[ACDeviceStateValue] = None
    eco: Optional[ACDeviceStateValue] = None
    nanoe: Optional[ACDeviceStateValue] = None
    
    def __init__(self) -> None:
        pass
    
    def __str__(self) -> str:
        return f"ACDeviceState(avail={self.available}, tIn={self.temperatureInside}, tOut={self.temperatureOutside}, t={self.temperature}, p={self.power}, m={self.mode}, fan={self.fanSpeed}, aH={self.airSwingHorizontal}, aV={self.airSwingVertical}, eco={self.eco}, nanoe={self.nanoe})"
    
    def normalize(self):
        if not self.power is None and not isinstance(self.power, ACDeviceStateValue):
            self.power = ACDeviceStateValue(int(self.power))
        if not self.mode is None and not isinstance(self.mode, ACDeviceStateValue):
            self.mode = ACDeviceStateValue(int(self.mode))
        if not self.temperature is None and not isinstance(self.temperature, float):
            self.temperature = float(self.temperature)
        
    # return true if current state has same goal state at the tested state
    def matches(self, test:"ACDeviceState"):
        if self.available is not None and self.available != test.available: return False
        if self.temperature is not None and self.temperature != test.temperature: return False
        
        if self.power is not None and self.power.matches(test.power): return False
        if self.mode is not None and self.mode.matches(test.mode): return False
        if self.fanSpeed is not None and self.fanSpeed.matches(test.fanSpeed): return False
        if self.airSwingHorizontal is not None and self.airSwingHorizontal.matches(test.airSwingHorizontal): return False
        if self.airSwingVertical is not None and self.airSwingVertical.matches(test.airSwingVertical): return False
        if self.eco is not None and self.eco.matches(test.eco): return False
        if self.nanoe is not None and self.nanoe.matches(test.nanoe): return False        
        return True
    
    @staticmethod
    def pccConstToData(obj):
        if issubclass(obj.__class__, Enum):
            return ACDeviceStateValue(obj.value, obj.name)
        raise Exception("Unknown type for enum convert: " + str(obj.__class__))
        #return super().default(obj)
    
    @staticmethod
    def createFromPcc(data) -> "ACDeviceState":
        obj = ACDeviceState()
        if data is None:
            obj.available = False
        else:
            if data is False or not "parameters" in data:
                raise Exception("Invalid data format: " + str(data))
            data = data["parameters"]
            obj.available = True
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