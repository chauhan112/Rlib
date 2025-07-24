from projects.data_server.lib import IPortal, Contact, PathPortal, Message
from modules.DataServer.FileObserve import ChangeModel, FilesLister, ChangeType
from CryptsDB import CryptsDB
import os
from Path import Path
from FileDatabase import File
from enum import Enum
class ServerOps(Enum):
    FileUploaded = 0
    Replace = 1
    SendFile = 2
    SendFiles = 3
class ICloudNode:
    def sync(self):
        pass
class PathSet:
    def set_path(self, path: str):
        self._path = path
        if not os.path.exists(path):
            os.makedirs(path)
    def send_message(self, msg: str, to: Contact):
        self._portal.write(Message({self._idd.getId(): msg}), to)
    def set_portal(self, portal: IPortal):
        self._portal = portal
    def read_message(self, delete_after= False):
        msg = self._portal.read(self._idd)
        if delete_after:
            self._portal.delete(self._idd)
        return msg
class Syncer:
    def set_message(self, msg):
        self._msg = msg
    def sync(self):
        msg = self._msg
        for msg in self._msg:
            for time in msg:
                message = msg[time]
                for person in message:
                    content = message[person]
                    if type(content) == dict:
                        for msg_type in content:
                            if msg_type in [ServerOps.FileUploaded.name, ChangeType.CREATED.name]:
                                self._created(content[msg_type], person)
                            elif msg_type == ChangeType.DELETED.name:
                                self._deleted(content[msg_type], person)
                            elif msg_type in [ServerOps.Replace.name, ChangeType.MODIFIED.name]:
                                self._replace(content[msg_type], person)
    def set_parent(self, parent: ICloudNode):
        self._parent = parent
        self._path = self._parent._path
        self._portal = self._parent._portal
    def _created(self, infos, von):
        for info in infos:
            name = info['name']
            loc = os.sep.join([self._path, info['loc']]).strip(os.sep)
            exisiting_file = os.sep.join([loc, info['original_name']])
            if os.path.exists(exisiting_file):
                print("file already exists")
                return
            self._portal.download_file(name, True, loc)
            File.rename(os.sep.join([loc, name]), exisiting_file)

    def _deleted(self, info, von):
        files = map(lambda x: os.sep.join([self._path, x]), info)
        files = filter(os.path.exists, files)
        File.deleteFiles(files)
    def _replace(self, infos, von):
        for info in infos:
            name = info['name']
            loc = os.sep.join([self._path, info['loc']]).strip(os.sep)
            self._portal.download_file(name, True, loc)
            existing_file = os.sep.join([loc, info['original_name']])
            if os.path.exists(existing_file):
                Path.delete([existing_file])
            File.rename(os.sep.join([loc, name]), existing_file)
class Server(ICloudNode, PathSet):
    def __init__(self, idd: str="server"):
        self._idd = Contact(idd)
        self._cm = None
        self._syncer = None
    def sync(self):
        if self._syncer is None:
            self._syncer = Syncer()
            self._syncer.set_parent(self)
        msg = self.read_message(True)
        if msg is None:
            return
        self._syncer.set_message(msg)
        self._syncer.sync()
class Client(ICloudNode, PathSet):
    def __init__(self):
        self._cm = None
    def set_id(self, idd: str):
        self._idd = Contact(idd)
    def sync(self):
        self._upload_changes()
        self._cm.update()
    def _download_changes(self):
        pass
    def _upload_changes(self):
        if self._cm is None:
            self._cm = ChangeModel()
            fl = FilesLister()
            fl.set_directory(self._path)
            self._cm.set_files_lister(fl)
        changes = self._cm.get_changes()

        
        # deleted
        msg = []
        delete_key = ChangeType.DELETED.name
        for f in changes[delete_key]:
            msg.append(self._cm.remove_path_prefix(f))
        if len(msg) > 0:
            self._portal.write(Message({self._idd.getId(): {delete_key: msg}}), self._server_id)
        # modified
        msg = []
        for f in changes[ChangeType.MODIFIED.name]:
            name = os.path.basename(f)
            new_name = self.upload_file(f)
            msg.append({ 'name' : new_name, 'original_name': name, 
                        'loc': os.path.dirname(self._cm.remove_path_prefix(f))})
        if len(msg) > 0:
            self._portal.write(Message({self._idd.getId(): {ServerOps.Replace.name: msg}}), self._server_id)
        
        # created
        msg = []
        for f in changes[ChangeType.CREATED.name]:
            name = os.path.basename(f)
            new_name = self.upload_file(f)
            msg.append({ 'name' : new_name, 'original_name': name, 
                        'loc': os.path.dirname(self._cm.remove_path_prefix(f))})
        if len(msg) > 0:
            self._portal.write(Message({self._idd.getId(): {ChangeType.CREATED.name: msg}}), self._server_id)
    def set_server_id(self, server_id: Contact):
        self._server_id = server_id
    def upload_file(self, file_path: str):
        name = os.path.basename(file_path)
        self._portal.upload_file(file_path)
        new_name = CryptsDB.generateRandomName()
        self._portal.rename_file(name, new_name)
        return new_name
    def download_file(self, file_location: str, to_path: str="."):
        self._portal.download_file(file_location, download_location = to_path)
    def server_files_explorer(self):
        pass
class Main:
    timer = None
    def sync_check( start=True):
        from ancient.Logger import GenericLogger
        s = Server()
        pp = PathPortal("cl")
        s.set_path("cl/server")
        s.set_portal(pp)
        c = Client()
        c.set_id("raja")
        c.set_path("here")
        c.set_portal(pp)
        c.set_server_id(s._idd)
        c.sync()
        gl = GenericLogger()
        gl.set_timer_interval(2)
        gl.add_log_func(c.sync)
        gl.add_log_func(s.sync)
        gl.start_auto_log()
        Main.timer = gl
        return gl