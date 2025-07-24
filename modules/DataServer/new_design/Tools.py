class IUnique:
    def get_id(self):
        pass
class IFile:
    def get_file_info(self) -> dict:
        pass
    def save_to(self, target_path: str):
        pass
    def get_path(self, filepath):
        pass
    def get_basename(self)-> str:
        pass
    def get_extension(self) -> str:
        pass
class IMessage:
    def get_content(self):
        pass
    def set_content(self, content):
        pass
    def get_files(self) -> list[IFile]:
        pass
class GMessage(IMessage, IUnique):
    def get_id(self):
        from useful.CryptsDB import CryptsDB
        return CryptsDB.generateUniqueId()
    def get_files(self):
        return []
class ILocation:
    def get_path(self):
        pass
class NameContact(IUnique):
    def __init__(self, name: str):
        self._name = name
    def get_id(self):
        return self._name
class INode:
    def send_message(self, msg: GMessage, to: NameContact):
        pass
    def get_all_messages(self) -> list:
        pass
class IPortal:
    def send_message(self, msg: GMessage, to: NameContact, von: NameContact):
        pass
    def get_all_messages(self, contact: IContact):
        pass
    def delete_messages(self, contact: IContact):
        pass
class TextMsg(GMessage):
    def __init__(self, txt):
        self.set_content(txt)
    def get_content(self):
        return self._txt
    def set_content(self, txt: str):
        self._txt = txt
class GNode(INode, IUnique):
    def __init__(self, idd: NameContact):
        self.set_contact_id(idd)
    def set_contact_id(self, c_id: NameContact):
        self._id = c_id
    def get_all_messages(self):
        return self._portal.get_all_messages(self._id)
    def set_portal(self, portal : IPortal):
        self._portal = portal
    def send_message(self, msg: GMessage, contact: NameContact):
        self._portal.send_message(msg, to=contact, von= self._id)
    def delete_all_messages(self):
        self._portal.delete_messages(self._id)
    def get_id(self):
        return self._id
from modules.DataServer.Tools import Tools
class GFile(IFile):
    def set_info(self, info):
        self._info = info
    def get_file_info(self):
        return self._info
    def get_path(self):
        return self._info['abs_path']
    def get_basename(self):
        return os.path.basename(self._info['abs_path'])
    def get_extension(self):
        return self._info['extension']
    def set_id(self, idd):
        self._idd = idd
    def get_id(self):
        return self._idd
class CustomMessage(IMessage, IUnique):
    def set_info(self, info):
        self._info = info
    def get_id(self):
        return self._info['id']
    def get_files(self):
        return self._files
    def set_files(self, files):
        self._files = files
    def get_content(self):
        return self._info['data']
    def get_more_info(self):
        return self._info
class FilePathPortal(IPortal):
    def set_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self._path = path
        self._files_dic_path = os.sep.join([self._path, "files_info.pkl"])
        if not os.path.exists(self._files_dic_path):
            SerializationDB.pickleOut({}, self._files_dic_path)
        self._messages_path = os.sep.join([self._path, "messages.pkl"])
        if not os.path.exists(self._messages_path):
            SerializationDB.pickleOut({}, self._messages_path)
        self._files_path = os.sep.join([self._path, "files"])
        if not os.path.exists(self._files_path):
            os.makedirs(self._files_path)
    def send_message(self, msg: GMessage, to: NameContact, von:NameContact):
        content = SerializationDB.readPickle(self._messages_path)
        if to.get_id() not in content:
            content[to.get_id()] = []
        content[to.get_id()].append(self._msg_instance(msg, von))
        SerializationDB.pickleOut(content, self._messages_path)
        for f in msg.get_files():
            self._move_file(f)
    def _msg_instance(self, msg: GMessage, con: NameContact):
        return {'data': msg.get_content(),
                'id': msg.get_id(),
                "from": con.get_id(),
                "time-stamp":  Tools.detailedTimeStamp(),
                "files": [f.get_id() for f in msg.get_files()]}
    def get_all_messages(self, node: NameContact):
        content = SerializationDB.readPickle(self._messages_path)
        messages = []
        for msg in content[node.get_id()]:
            messages.append(self.load_message(msg))
        return messages
    def load_message(self, msg):
        files_content = SerializationDB.readPickle(self._files_dic_path)
        ins_msg = CustomMessage()
        ins_msg.set_info(msg)
        files = []
        for f in msg['files']:
            fls = GFile()
            fls.set_id(f)
            fls.set_info(files_content[f])
            files.append(fls)
        ins_msg.set_files(files)
        return ins_msg
    def delete_messages(self, node: NameContact):
        content = SerializationDB.readPickle(self._messages_path)
        files_content = SerializationDB.readPickle(self._files_dic_path)
        messages = content[node.get_id()]
        files = []
        for msg in messages:
            for f in msg['files']:
                files.append(files_content[f]['path'])
                del files_content[f]
        Path.delete(files)
        del content[node.get_id()]
        SerializationDB.pickleOut(content, self._messages_path)
        SerializationDB.pickleOut(files_content, self._files_dic_path)
    def _move_file(self, file: IFile):
        content = SerializationDB.readPickle(self._files_dic_path)
        path = file.get_path()
        idd = file.get_id()
        if idd not in content:
            Path.copyFiles([path], self._files_path)
            new_path = self._files_path + os.sep + idd + '.' +  file.get_extension()
            File.rename(self._files_path + os.sep + file.get_basename(),
                        new_path)
            content[idd] = file.get_file_info()
            content[idd]['path'] = new_path
            SerializationDB.pickleOut(content, self._files_dic_path)