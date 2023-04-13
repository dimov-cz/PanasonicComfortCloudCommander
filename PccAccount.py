import time
import random
import logging
from typing import Optional, List
try:
    from .pccLocal.pcomfortcloud import Session as pccSession
    from .pccLocal.pcomfortcloud import Error as pccError
    from .pccLocal.pcomfortcloud import LoginError as pccLoginError
    from .pccLocal.pcomfortcloud import ResponseError as pccResponseError
    logging.getLogger().warn("Using local pcomfortcloud Session")
except ImportError:
    from pcomfortcloud import Session as pccSession

globalCommunicationLockTime = 0
delockTimeInterval = 15 # seconds

class PccAccount:
    login: Optional[str] = None
    password: Optional[str] 
    tokenPath: str
    session: Optional[pccSession] = None
    deviceInfoUpdateInProgress: dict = {}
    def __init__(self, login: str, password: str, tokenPath: str) -> None:
        self.login = login
        self.password = password
        self.tokenPath = tokenPath
    def __str__(self) -> str:
        return f"AccountInfo(login={self.login}, password={self.password}, tokenPath={self.tokenPath}, session={self.session})"
    
    def __hasSession(self):
        return self.session != None
    
    def __getSession(self):
        if not self.__hasSession():
            self.session = self.__createSession()
        return self.session
    
    def __createSession(self):
        self.session = pccSession(self.login, self.password, self.tokenPath)
        return self.session

    def __doAction(self, action):
        global globalCommunicationLockTime
        while True:
            try:
                # Wait for global lock to be released
                while globalCommunicationLockTime > time.time():
                    time.sleep(delockTimeInterval + random.randint(-20, 20)/10) # +- 2 seconds
                    
                return action()
            except pccResponseError as e:            
                if e.status_code == 429:
                    logging.warning(f"Action failed on {self.login}: Too many requests - retrying in {delockTimeInterval} seconds")
                    globalCommunicationLockTime = time.time() + delockTimeInterval
                    time.sleep(15 + random.randint(-20, 20)/10) # +- 2 seconds
                elif e.status_code == 500:
                    logging.info(f"Server or connection error on {self.login}: " + e.text)
                    #TODO process this availabality status
                    return None
                else:
                    logging.error(f"Action failed on {self.login}: " + str(e.status_code) + " / " + str(e.args))
                    return None
            except pccLoginError as e:
                logging.error(f"Login failed for account {self.login}")
                return None
            except Exception as e:
                logging.error(f"Action failed on {self.login}: " + str(e))
                return None
    
    def getDevices(self) -> Optional[List]:
        return self.__doAction(lambda: self.__getSession().get_devices());
    
    """ returns True if update is in progress
        There is no sense to have multiple update requests for the same device at the same time
        This avoids cumulating request when the server is not responding
    """
    def getDevice(self, ppcId):
        if self.deviceInfoUpdateInProgress.get(ppcId, False):
            logging.debug(f"Get device info update already in progress for {ppcId}")
            return True
        self.deviceInfoUpdateInProgress[ppcId] = True
        result = self.__doAction(lambda: self.__getSession().get_device(ppcId));
        self.deviceInfoUpdateInProgress[ppcId] = False
        return result
    
    def setDevice(self, ppcId, **kwargs):
        self.__getSession()._raw = True
        return self.__doAction(lambda: self.__getSession().set_device(ppcId, **kwargs));
