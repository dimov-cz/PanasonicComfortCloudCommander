import threading
from .ACDevice import ACDevice
from .ResponsesQueue import ResponsesQueue
from .Response import Response

class CommandExecutionThread(threading.Thread):
    acDevice: ACDevice = None
    responseQueue: ResponsesQueue = None
    command = None
    commandId = None
    
    def __init__(self, commandId: int, acDevice: ACDevice, command, responseQueue: ResponsesQueue, arg1: str) -> None:
        self.commandId = commandId
        self.acDevice = acDevice
        self.responseQueue = responseQueue
        self.command = command
        self.arg1 = arg1
        super().__init__(name=f"Thread #{commandId} for " + acDevice.acDevice.name + " (" + command + ")")
    def addResponse(self, type: str, data):
        self.responseQueue.add(Response(self.commandId, self.acDevice, type, data))
        
    def run(self):
        print(f"Executing command '{self.command}' for device {self.acDevice.acDevice.name}")
        
        updateStatus = True #most commands will update status
        if self.command == "status":
            pass #do nothing, status will be updated later
        elif self.command == "setpower":
            self.acDevice.setPower(self.arg1)
        elif self.command == "setmode":
            self.acDevice.setMode(self.arg1)
        elif self.command == "settemp":
            self.acDevice.setTemperature(self.arg1)
        else:
            updateStatus = False
        
        if updateStatus:
            status = self.acDevice.getStatus()
            if status == None:
                self.addResponse('error', "Failed to get status or another update already in progress")
            elif status != True: #True means status is updated already by another command
                self.addResponse('status', status)