from typing import Optional, Union
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
    
    #true if status update already in progress
    def getStatus(self) -> Union[ACDeviceState, bool]:
        data = self.readAccount.getDevice(self.acDevice.deviceId)
        if data is True:
            return True
        logging.getLogger().debug(f"Got device status: {data}")
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
        if state.eco is not None:
            kwargs["eco"] = pccConstants.EcoMode(state.eco.value)
        if state.fanSpeed is not None:
            kwargs["fanSpeed"] = pccConstants.FanSpeed(state.fanSpeed.value)
        if state.airSwingVertical is not None:
            kwargs["airSwingVertical"] = pccConstants.AirSwingUD(state.airSwingVertical.value)
        if state.airSwingHorizontal is not None:
            kwargs["airSwingHorizontal"] = pccConstants.AirSwingLR(state.airSwingHorizontal.value)
        if state.nanoe is not None:
            kwargs["nanoe"] = pccConstants.NanoeMode(state.nanoe.value)            
        
        self.writeAccount.setDevice(self.acDevice.deviceId, **kwargs)
        
    def setPower(self, state):
        try:
            stateConst = pccConstants.Power[state]
        except KeyError:
            stateConst = pccConstants.Power(int(state))
        self.writeAccount.setDevice(self.acDevice.deviceId, power = stateConst)
        
    def setMode(self, state):
        try:
            stateConst = pccConstants.OperationMode[state]
        except KeyError:
            stateConst = pccConstants.OperationMode(int(state))
        self.writeAccount.setDevice(self.acDevice.deviceId, mode = stateConst)
        
    def setTemperature(self, temperature):
        self.writeAccount.setDevice(self.acDevice.deviceId, temperature = temperature)