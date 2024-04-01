from typing import Optional
import threading
import logging
from .ACDevice import ACDevice
from .ACDeviceState import ACDeviceState
from .ResponsesQueue import ResponsesQueue
from .Response import Response
from .ResponseType import ResponseType
from .Request import Request
from .RequestType import RequestType

class RequestExecutionThread(threading.Thread):
    request: Request
    responseQueue: ResponsesQueue
    
    def __init__(self, request: Request, responseQueue: ResponsesQueue) -> None:
        self.logger = logging.getLogger(__class__.__name__)
        self.request = request
        self.responseQueue = responseQueue
        super().__init__(name=f"RequestExecutionThread({request})")
        
    def setLogLevel(self, level):
        self.logger.setLevel(level)
        
    def addResponse(self, type: ResponseType, data, device: Optional[ACDevice] = None):
        self.responseQueue.add(Response(type, device, data))
        
    def run(self):
        self.logger.debug(f"Executing request {self.request}")
        updateStatus = False
        
        if (self.request.type == RequestType.ListDevices):
            devices = self.request.account.getDevices()
            if devices == None:
                self.addResponse(ResponseType.Error, "Failed to get devices", None)
                return
            for device in devices:
                self.addResponse(ResponseType.PreRegistration, { 'device': device, 'account': self.request.account }, None)
        
        elif (self.request.type == RequestType.Status):
            updateStatus = True
        
        elif self.request.type == RequestType.SetState:
            #check if self.request.data is instance of ACDeviceState
            
            if not isinstance(self.request.data, ACDeviceState):
                self.addResponse(ResponseType.Error, "Invalid data for state", None)
                return
            state: ACDeviceState = self.request.data
            if not isinstance(self.request.device, ACDevice):
                self.addResponse(ResponseType.Error, "Invalid device for state", None)
                return
            device: ACDevice = self.request.device
            self.request.device.setState(state)
            updateStatus = True
                
        
        if updateStatus:
            status = self.request.device.getStatus()
            if status == True:
                return
            elif isinstance(status, ACDeviceState):
                self.addResponse(ResponseType.Status, status, self.request.device)
            else:
                self.addResponse(ResponseType.Error, "Failed to update status", self.request.device)
