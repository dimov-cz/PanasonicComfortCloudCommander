import logging
from typing import Optional, Dict
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
    accounts = []
    presets: Dict[str, ACDeviceState] = {}
    
    devices = {}
    responseQueue = ResponsesQueue()
    
    def __init__(self, presets: Dict[str, ACDeviceState] = {}, logLevel = logging.INFO) -> None:        
        self.logger = logging.getLogger(__name__)
        self.setLogLevel(logLevel)
        self.presets["none"] = ACDeviceState()
        self.presets.update(presets)
            
    def setLogLevel(self, level):
        self.logger.setLevel(level)
            
    def addAccount(self, login, password, tokenPath):
        try:
            newAccount = PccAccount(login, password, tokenPath)
            self.accounts.append(newAccount)
            self.logger.info(f"Account {login} added successfully")
            self._registerAccountDevices(newAccount)
        except Exception as e:
            self.logger.error(f"Failed to add account {login}: {e}")
            return False
        return True
    
    def getPresetsIds(self) -> list:
        return list(self.presets.keys())
    
    def getPresetState(self, presetId) -> ACDeviceState:
        if presetId not in self.presets:
            raise Exception(f"Preset with id {presetId} not found")
        return self.presets[presetId]
    
    def getPresetsIdFromState(self, state: ACDeviceState) -> Optional[str]:
        for presetId, presetState in self.presets.items():
            if presetId == "none":
                continue
            #self.logger.debug(f"Comparing {presetState} with {state}")
            if presetState.matches(state):
                self.logger.debug(f"Current state matchs preset {presetId}")
                return presetId
        return "none"
    
    def _registerAccountDevices(self, account: PccAccount):
        self._sendRequest(Request(type=RequestType.ListDevices, account=account, device=None, data=None))
    
    def getDevicesList(self):
        return [device.getDeviceInfo().getData() for device in self.devices.values()]
    
    def hasDevice(self, deviceId) -> bool:
        return deviceId in self.devices
    
    def _sendRequest(self, request: Request):
        thread = RequestExecutionThread(request, self.responseQueue)
        thread.setLogLevel(self.logger.getEffectiveLevel())
        thread.start()
        
    def requestReannounce(self):
        for device in self.devices.values():
            response = Response(ResponseType.Registration, device, None)
            self.responseQueue.add(response)
            
    def requestStatus(self, deviceId):
        try:
            if deviceId not in self.devices:
                raise Exception(f"Device with deviceId {deviceId} not found")
            self._sendRequest(Request(type=RequestType.Status, device=self.devices[deviceId]))
        except Exception as e:
            self.responseQueue.add(Response(ResponseType.Error, None, str(e)))
        
    def requestStatusAll(self):
        for device in self.devices:
            self.requestStatus(device)
            
    def requestSetState(self, deviceId, state: ACDeviceState):
        self._sendRequest(Request(type=RequestType.SetState, device=self.devices[deviceId], data=state))
        
    def getResponse(self) -> Optional[Response]:
        response = self.responseQueue.get()
        if (response == None):
            return None
        
        if response.type == ResponseType.PreRegistration: #not for controllers, convert to registration
            self.logger.debug(f"Registration response: {response}")
            if response.data is None:
                self.logger.error(f"Registration response data is None")
                return self.getResponse()
            device = response.data['device']
            account = response.data['account']
            deviceId = device["id"]
            if deviceId in self.devices:
                self.devices[deviceId].updateReadAccount(account)
                self.devices[deviceId].updateWriteAccount(account)
                self.logger.info(f"Updated device {deviceId} accounts to {account.login}")
                #not significant, return next response
                return self.getResponse()
            else:
                newDeviceInfo = ACDeviceInfo(deviceId, device["name"], device["group"], device["model"], self.presets)
                newDevice = ACDevice(newDeviceInfo, account, account)
                self.devices[deviceId] = newDevice
                self.logger.info(f"Registered new device {deviceId}")
                #upgrade to new response:
                response = Response(ResponseType.Registration, newDevice)
        elif response.type == ResponseType.Status:
            if isinstance(response.data, ACDeviceState):
                if response.data.available:
                    response.data.presetId = self.getPresetsIdFromState(response.data)
        elif response.type == ResponseType.Error:
            self.logger.error(f"Error response: {response.data}")
        elif response.type == ResponseType.Registration:
            self.logger.error(f"Unexpected registration response: {response}")
        else:
            self.logger.error(f"Got response: {response}")


        
        logging.debug(f"Delivering response: {response}")
        return response
    
