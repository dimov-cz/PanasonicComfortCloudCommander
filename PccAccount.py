try:
    from .pccLocal.pcomfortcloud import Session as pccSession
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
    
    def hasSession(self):
        return self.session != None
    
    def getSession(self):
        if not self.hasSession():
            self.session = self.createSession()
        return self.session
    
    def createSession(self):
        self.session = pccSession(self.login, self.password, self.tokenPath)
        return self.session