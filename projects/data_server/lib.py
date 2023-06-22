from modules.DataServer.Interfaces import IContact, IMessage
from modules.DataServer.Tools import Tools
import os
from SerializationDB import SerializationDB
from Path import Path
from FileDatabase import File

class IPortal:
    def write(self, message:IMessage, to: IContact):
        pass
    def read(self, von: IContact):
        pass
    def upload_file(self, filePath: str):
        pass
    def download_file(self, identifier, delete_original=True): # deletes files from portal
        pass
    def rename_file(self, original_id, new_id):
        pass
class Message(IMessage):
    def __init__(self, content):
        self._content = content
    def get(self):
        return self._content
    def get_message_with_timestamp(self):
        return {Tools.detailedTimeStamp(): self.get()}
class PathPortal(IPortal):
    def __init__(self, path:str= None):
        self._pkl_name = "msg.pkl"
        self._files_section = "files"
        if path is not None:
            self.set_path(path)
    def set_path(self, path: str):
        self._path = path
        if not os.path.exists(self._path):
            os.makedirs(self._path)
    def write(self, message: Message, to: IContact):
        content = self._get_content()
        if to.getId() not in content:
            content[to.getId()] = []
        content[to.getId()].append(message.get_message_with_timestamp())
        self._write_content(content)
    def _get_content(self):
        msg_pkl = os.sep.join([self._path, self._pkl_name])
        if not os.path.exists(msg_pkl):
            SerializationDB.pickleOut({}, msg_pkl)
        content = SerializationDB.readPickle(msg_pkl)
        return content
    def _write_content(self, content):
        SerializationDB.pickleOut(content, os.sep.join([self._path, self._pkl_name]))
    def read(self, von:IContact):
        content = self._get_content()
        if von.getId() in content:
            return content[von.getId()]
    def upload_file(self, file_path: str):
        files_folder = os.sep.join([self._path, self._files_section])
        if not os.path.exists(files_folder):
            os.makedirs(files_folder)
        file = os.sep.join([files_folder, os.path.basename(file_path)])
        Path.copyFiles([file_path], files_folder)
    def download_file(self, file_name, delete_original=True, download_location = "."):
        basename = os.path.basename(file_name)
        file_on_server = os.sep.join([self._path, self._files_section, basename])
        if os.path.exists(file_on_server):
            if not delete_original:
                Path.copyFiles([file_on_server], download_location)
            else:
                Path.move().files([file_on_server], download_location)
        else:
            print ("file does not exist")
        
    def rename_file(self, oldname, newname):
        files_folder = os.sep.join([self._path, self._files_section])
        old = os.sep.join([files_folder, os.path.basename(oldname)])
        new = os.sep.join([files_folder, os.path.basename(newname)])
        File.rename(old, new)
    def delete(self, of: IContact):
        content = self._get_content()
        if of.getId() in content:
            del content[of.getId()]
            self._write_content(content)
class Contact(IContact):
    def __init__(self, idd):
        self._idd = idd
    def getId(self):
        return self._idd