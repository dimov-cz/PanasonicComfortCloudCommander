#implement enum for response types
from enum import Enum

class ResponseType(Enum):
    PreRegistration = "reg"
    Registration = "ann"
    Status = "status"
    Error = "error"
    