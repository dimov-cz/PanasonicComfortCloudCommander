from .ACDevice import ACDevice
from .ACDeviceInfo import ACDeviceInfo
from .PccAccount import PccAccount
from .Response import Response
from .ResponsesQueue import ResponsesQueue
from .CommandExecutionThread import CommandExecutionThread

class PccCommander:
    mainAccount = None
    subAccounts = []
    
    devices = {}
    responseQueue = None
    commandIdx: int = 1000
    
    def __init__(self, login, password, tokenPath) -> None:        
        self.responseQueue = ResponsesQueue()
        self.mainAccount = PccAccount(login, password, tokenPath)
        self.registerAccountDevices(self.mainAccount) #also checks connectivity, password etc...
            
    def addSubAccount(self, login, password, tokenPath):
        try:
            subAccount = PccAccount(login, password, tokenPath)
            self.subAccounts.append(subAccount)
            print(f"Subaccount {login} added")
            self.registerAccountDevices(subAccount, True)
        except Exception as e:
            print(f"Failed to add subaccount {login}: {e}")
            return False
        return True
    
    def registerAccountDevices(self, account: PccAccount, prefferedForWrite=False):
        devices = account.getDevices()
        if devices == None:
            raise Exception(f"Failed to register account {account.login}")
        
        print(f"Registering {len(devices)} devices for account {account.login}")
        for item in devices:
            deviceId = self.calcDeviceId(item["id"])
            if deviceId in self.devices:
                if prefferedForWrite:
                    self.devices[deviceId].updateReadAccount(account)
                    self.devices[deviceId].updateWriteAccount(account)
                    print(f"Existing device accounts updated: {self.devices[deviceId]}")
            else:
                newDeviceInfo = ACDeviceInfo(deviceId, item["id"], item["name"], item["group"], item["model"])
                newDevice = ACDevice(newDeviceInfo, account, account)
                self.devices[deviceId] = newDevice
                print(f"New device: {newDevice}")
    
    def getDevicesList(self):
        return [device.getDeviceInfo().getData() for device in self.devices.values()]
    
    def getNewCommandId(self):
        commandId = self.commandIdx
        self.commandIdx += 1
        return commandId
    
    def fireCommand(self, deviceId, command, arg1 = None) -> int:
        commandId = self.getNewCommandId()
        
        if deviceId == "all":
            if command == "list":
                self.responseQueue.add(Response(commandId, None, "list", self.getDevicesList()))
                return commandId
            else:
                for device in self.devices.values():
                    self.fireCommand(device.getDeviceInfo().getDeviceId(), command, arg1)
                return 0
        else:
            if deviceId not in self.devices:
                raise Exception(f"Device with deviceId {deviceId} not found")
            thread = CommandExecutionThread(commandId, self.devices[deviceId], command, self.responseQueue, arg1)
            thread.start()
            
        return commandId
        
    def getResponse(self):
        response = self.responseQueue.get()
        if (response == None):
            return None
        #print(f"Delivering response: {response}")
        return response
    
    #creates shorter hash from pcc guid to use as deviceId
    #this helps integrate with other systems
    def calcDeviceId(self, long_hash):
        # Convert hex to bytes
        hash_bytes = bytes.fromhex(long_hash)

        # Sum first 8 bytes XOR last 8 bytes
        sum_bytes = hash_bytes[:8] + hash_bytes[-8:]
        sum_value = bytes(x ^ y for x, y in zip(sum_bytes[:8], sum_bytes[8:]))

        # Convert 8-byte value to hex 
        short_hash = hex(int.from_bytes(sum_value, byteorder='big'))[2:]
        return short_hash