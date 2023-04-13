#implement enum for response types
from enum import Enum

class ResponseType(Enum):
    Registration = "reg"
    Announcement = "ann"
    RegistrationList = "reg-list"
    Status = "status"
    Error = "error"
    