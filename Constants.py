import logging

try:
    from .pccLocal.pcomfortcloud.constants import Power, OperationMode, AirSwingAutoMode, AirSwingLR, AirSwingUD, EcoMode, FanSpeed, dataMode, NanoeMode
    logging.getLogger().warn("Using local pcomfortcloud constants")
except ImportError:
    from pcomfortcloud.constants           import Power, OperationMode, AirSwingAutoMode, AirSwingLR, AirSwingUD, EcoMode, FanSpeed, dataMode, NanoeMode


