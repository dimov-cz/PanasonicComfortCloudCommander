
class ACDeviceInfo:
    
    def __init__(self, deviceId, pccId, name, group, model, presets: dict) -> None:
        self.deviceId = deviceId
        self.pccId = pccId
        self.name = name
        self.group = group
        self.model = model
        self.presets = presets
        
    def __str__(self) -> str:
        return f"ACDeviceInfo(deviceId={self.deviceId}, ppcId={self.pccId} name={self.name}, group={self.group}, model={self.model})"
    
    def getDeviceId(self):
        return self.deviceId
    
    def getData(self):
        return {
            "id": self.deviceId,
            "name": self.name,
            "group": self.group,
            "model": self.model,
            "presets": self.presets
        }