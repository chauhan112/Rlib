
class SystemInfo:
    def getName():
        import socket
        return socket.gethostname()
    def isLinux():
        import os
        return os.name != 'nt'
            
