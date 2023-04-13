from enum import Enum

class RequestType(Enum):
    ListDevices = "list-devices"
    Status = "status"
    SetState = "set-state"
    SetTargetTemperature = "set-temp"