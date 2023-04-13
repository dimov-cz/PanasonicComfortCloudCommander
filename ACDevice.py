from typing import Optional
import logging
from .ACDeviceInfo import ACDeviceInfo
from .PccAccount import PccAccount
from .ACDeviceState import ACDeviceState
from .ACDeviceStateValue import ACDeviceStateValue

try:
    from .pccLocal.pcomfortcloud import constants as pccConstants
    logging.getLogger().warn("Using local pcomfortcloud constants")
except ImportError:
    from pcomfortcloud import constants as pccConstants

class ACDevice:
    readAccount:PccAccount
    writeAccount:PccAccount
    
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
    
    def getStatus(self) -> ACDeviceState:
        data = self.readAccount.getDevice(self.acDevice.pccId)
        state = ACDeviceState.createFromPcc(data)
        return state
        
    def setState(self, state: ACDeviceState):
        state.normalize()
        kwargs = {}
        if state.power is not None:
            kwargs["power"] = pccConstants.Power(state.power.value)
        if state.mode is not None:
            kwargs["mode"] = pccConstants.OperationMode(state.mode.value)
        if state.temperature is not None:
            kwargs["temperature"] = state.temperature
        
        self.writeAccount.setDevice(self.acDevice.pccId, **kwargs)
        
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