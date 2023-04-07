from . import ACDeviceInfo
from . import PccAccount

try:
    from .pccLocal.pcomfortcloud import constants as pccConstants
    print("Using local pcomfortcloud constants")
except ImportError:
    from pcomfortcloud import constants as pccConstants

class ACDevice:
    def __init__(self, acDevice: ACDeviceInfo, readAccount: PccAccount, writeAccount: PccAccount) -> None:
        self.acDevice = acDevice
        self.readAccount = readAccount
        self.writeAccount = writeAccount
        
    def __str__(self) -> str:
        return f"ACDevice(acDevice={self.acDevice}, readAccount={self.readAccount.login}, writeAccount={self.writeAccount.login})"
    
    def updateWriteAccount(self, writeAccount: PccAccount):
        self.writeAccount = writeAccount
        
    def getDeviceInfo(self):
        return self.acDevice
    
    def getStatus(self):
        status = self.readAccount.getSession().get_device(self.acDevice.pccId)
        return status
    def setPower(self, state):
        try:
            stateConst = pccConstants.Power[state]
        except KeyError:
            stateConst = pccConstants.Power(int(state))
        self.writeAccount.getSession().set_device(self.acDevice.pccId, power = stateConst)
    def setMode(self, state):
        try:
            stateConst = pccConstants.OperationMode[state]
        except KeyError:
            stateConst = pccConstants.OperationMode(int(state))
        self.writeAccount.getSession().set_device(self.acDevice.pccId, mode = stateConst)
    def setTemperature(self, temperature):
        self.writeAccount.getSession().set_device(self.acDevice.pccId, temperature = temperature)