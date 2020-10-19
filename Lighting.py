from phue import Bridge

class Lighting():
    def __init__(self,ip_addr):
        self.b=Bridge(ip_addr)