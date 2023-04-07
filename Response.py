from .ACDevice import ACDevice

class Response:
    def __init__(self, commandId, acDevice: ACDevice, type: str, data) -> None:
        self.commandId = commandId
        self.acDevice = acDevice
        self.type = type
        self.data = data
    def __str__(self) -> str:
        return f"Response(commandId={self.commandId}, acDevice={self.acDevice}, type={self.type}, data={self.data})"

