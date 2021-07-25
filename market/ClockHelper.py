from datetime import datetime

class CHelper:

    def __init__(self) -> None:
        self.dtime = datetime
        pass

    def hora(self):
        return self.dtime.now().strftime('%H')
    
    def min(self):
        return self.dtime.now().strftime('%M')
    