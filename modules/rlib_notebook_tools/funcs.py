import os
class Tools:
    def cmdAtPath(path):
        from OpsDB import OpsDB
        fullpath = os.path.abspath(path)
        volumeLabel = fullpath[:2]
        OpsDB.cmd().onthread([volumeLabel, f'cd "{fullpath}"', "start"])