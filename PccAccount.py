import time
try:
    from .pccLocal.pcomfortcloud import Session as pccSession
    from .pccLocal.pcomfortcloud import Error as pccError
    from .pccLocal.pcomfortcloud import LoginError as pccLoginError
    from .pccLocal.pcomfortcloud import ResponseError as pccResponseError
    print("Using local pcomfortcloud Session")
except ImportError:
    from pcomfortcloud import Session as pccSession

class PccAccount:
    login = None
    password = None
    tokenPath = None
    session = None
    def __init__(self, login, password, tokenPath) -> None:
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

    def __doAction(self, action: callable):
        while True:
            try:
                return action()
            except pccResponseError as e:            
                if e.status_code == 429:
                    print(f"Action failed on {self.login}: Too many requests - retrying in 15 seconds")
                    time.sleep(15)
                else:
                    print(f"Action failed on {self.login}: " + str(e.status_code))
                    return None
            except pccLoginError as e:
                print(f"Login failed for account {self.login}")
                return None
            except Exception as e:
                print(f"Action failed on {self.login}: " + str(e))
                return None
    
    def getDevices(self):
        return self.__doAction(lambda: self.__getSession().get_devices());
    
    def getDevice(self, ppcId):
        return self.__doAction(lambda: self.__getSession().get_device(ppcId));
    
    def setDevice(self, ppcId, **kwargs):
        return self.__doAction(lambda: self.__getSession().set_device(ppcId, **kwargs));
