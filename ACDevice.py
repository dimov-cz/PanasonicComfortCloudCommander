from . import ACDeviceInfo
from . import PccAccount

try:
    from .pccLocal.pcomfortcloud import constants as pccConstants
    print("Using local pcomfortcloud constants")
except ImportError:
    from pcomfortcloud import constants as pccConstants

class ACDevice:
    readAccount: PccAccount = None
    writeAccount: PccAccount = None
    
    def __init__(self, acDevice: ACDeviceInfo, readAccount: PccAccount, writeAccount: PccAccount) -> None:
        self.acDevice = acDevice
        self.readAccount = readAccount
        self.writeAccount = writeAccount
        
    def __str__(self) -> str:
        return f"ACDevice(acDevice={self.acDevice}, readAccount={self.readAccount.login}, writeAccount={self.writeAccount.login})"
    
    def updateWriteAccount(self, account: PccAccount):
        self.writeAccount = account
    def updateReadAccount(self, account: PccAccount):
        self.readAccount = account
        
    def getDeviceInfo(self):
        return self.acDevice
    
    def getStatus(self):
        return self.readAccount.getDevice(self.acDevice.pccId)
        
    def setPower(self, state):
        try:
            stateConst = pccConstants.Power[state]
        except KeyError:
            stateConst = pccConstants.Power(int(state))
        self.writeAccount.setDevice(self.acDevice.pccId, power = stateConst)
        
    def setMode(self, state):
        try:
            stateConst = pccConstants.OperationMode[state]
        except KeyError:
            stateConst = pccConstants.OperationMode(int(state))
        self.writeAccount.setDevice(self.acDevice.pccId, mode = stateConst)
        
    def setTemperature(self, temperature):
        self.writeAccount.setDevice(self.acDevice.pccId, temperature = temperature)