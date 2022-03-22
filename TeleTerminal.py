import os
import subprocess
import tempfile

class TeleTerminal:
    def command(cmd):
        res = subprocess.run(cmd, shell= True, capture_output= True, text = True)
        return res.stdout

    def sudoCommand(command, password):
        command = command.split(" ")
        if(command[0] == "sudo"):
            command = " ".join(command[1:])
        else:
            command = " ".join(command)
        return os.system('echo %s|sudo -S %s' % (password, command))

    