import logging
from .ACDevice import ACDevice
from .ACDeviceInfo import ACDeviceInfo
from .PccAccount import PccAccount
from .Response import Response
from .ResponsesQueue import ResponsesQueue
from .ResponseType import ResponseType
from .Request import Request
from .RequestType import RequestType
from .RequestExecutionThread import RequestExecutionThread
from .ACDeviceState import ACDeviceState

class PccCommander:
    mainAccount = None
    subAccounts = []
    presets = {}
    
    devices = {}
    responseQueue = ResponsesQueue()
    
    def __init__(self, login, password, tokenPath, presets: dict, logLevel = logging.INFO) -> None:        
        self.logger = logging.getLogger(__name__)
        self.setLogLevel(logLevel)
        
        self.mainAccount = PccAccount(login, password, tokenPath)
        self.presets = presets
        
        self.registerAccountDevices(self.mainAccount)
    
    def setLogLevel(self, level):
        self.logger.setLevel(level)
            
    def addSubAccount(self, login, password, tokenPath):
        try:
            subAccount = PccAccount(login, password, tokenPath)
            self.subAccounts.append(subAccount)
            self.logger.info(f"Subaccount {login} added")
            self.registerAccountDevices(subAccount)
        except Exception as e:
            self.logger.error(f"Failed to add subaccount {login}: {e}")
            return False
        return True
    
    def registerAccountDevices(self, account: PccAccount):
        self.sendRequest(Request(type=RequestType.ListDevices, account=account, device=None, data=None))
    
    def getDevicesList(self):
        return [device.getDeviceInfo().getData() for device in self.devices.values()]
    
    def sendRequest(self, request: Request):
        thread = RequestExecutionThread(request, self.responseQueue)
        thread.setLogLevel(self.logger.getEffectiveLevel())
        thread.start()
        
    def requestReannounce(self):
        for device in self.devices.values():
            response = Response(ResponseType.Announcement, device, None)
            self.responseQueue.add(response)
            
    def requestStatus(self, deviceId):
        try:
            if deviceId not in self.devices:
                raise Exception(f"Device with deviceId {deviceId} not found")
            self.sendRequest(Request(type=RequestType.Status, device=self.devices[deviceId]))
        except Exception as e:
            self.responseQueue.add(Response(ResponseType.Error, None, str(e)))
        
    def requestStatusAll(self):
        for device in self.devices:
            self.requestStatus(device)
            
    def requestSetState(self, deviceId, state: ACDeviceState):
        self.sendRequest(Request(type=RequestType.SetState, device=self.devices[deviceId], data=state))
        
    def getResponse(self):
        response = self.responseQueue.get()
        if (response == None):
            return None
        
        if response.type == ResponseType.Registration: #not for controllers, convert to announcement
            self.logger.debug(f"Registration response: {response}")
            device = response.data['device']
            account = response.data['account']
            deviceId = self.calcDeviceId(device["id"])
            if deviceId in self.devices:
                self.devices[deviceId].updateReadAccount(account)
                self.devices[deviceId].updateWriteAccount(account)
                self.logger.info(f"Updated device {deviceId} accounts to {account.login}")
                #not significant, return next response
                return self.getResponse()
            else:
                newDeviceInfo = ACDeviceInfo(deviceId, device["id"], device["name"], device["group"], device["model"], self.presets)
                newDevice = ACDevice(newDeviceInfo, account, account)
                self.devices[deviceId] = newDevice
                self.logger.info(f"Registered new device {deviceId}")
                #upgrade to new response:
                response = Response(ResponseType.Announcement, newDevice, None)
                
        
        logging.debug(f"Delivering response: {response}")
        return response
    
    #creates shorter hash from pcc guid to use as deviceId
    #this helps integrate with other systems
    @staticmethod
    def calcDeviceId(long_hash):
        # Convert hex to bytes
        hash_bytes = bytes.fromhex(long_hash)

        # Sum first 8 bytes XOR last 8 bytes
        sum_bytes = hash_bytes[:8] + hash_bytes[-8:]
        sum_value = bytes(x ^ y for x, y in zip(sum_bytes[:8], sum_bytes[8:]))

        # Convert 8-byte value to hex 
        short_hash = hex(int.from_bytes(sum_value, byteorder='big'))[2:]
        return short_hash