import os
from OpsDB import IOps, OpsDB

class GitPortalInstantiate(IOps):
    def __init__(self, path):
        self.url = "git@github.com:chauhan112/DataServer.git"
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path
    def execute(self):
        targetFolder = self.path + os.sep + 'DataServer'
        if os.path.exists(targetFolder):
            return targetFolder
        curpath = os.getcwd()
        os.chdir(self.path)
        OpsDB.cmd().run(f'git clone {self.url}')
        os.chdir(curpath)
        return targetFolder

class Tools:
    def detailedTimeStamp():
        from TimeDB import TimeDB
        from WordDB import WordDB
        stamp = TimeDB.getTimeStamp()
        clockTime =":".join(list(map(lambda x: WordDB.formatting().integer(x, 2, '0'), TimeDB.nowTime())))
        return stamp+ "  "+clockTime
        
    def copyFromServer(waitsFor = 60):
        from ancient.ClipboardDB import ClipboardDB
        server = GitContact("server")
        portal.sendMessage(CopyMeClipCommand, server)
        ti = 0
        while True:
            wait(sec =10)
            ti +=10
            if(copied or ti> waitsFor):
                break
        msg = portal.receiveMessage(thisContact) # list of dict
        msgS = filterMsg(msg, {'from': server}) # list of dict
        msgContent = getContent(msg) # list
        ClipboardDB.copy2clipboard(msg[-1]) # copies last content

class GoogleDrive:
    def __init__(self):
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive
        gauth = GoogleAuth()           
        self._drive = GoogleDrive(gauth)
        self._default_folder = "1QzDlAO0iexXHFlNQuHlmvtcW2d8NTdjQ"

    def file_crud(self):
        class Temp:
            def upload(file_path):
                gfile = self._drive.CreateFile({'parents': [{'id': '1QzDlAO0iexXHFlNQuHlmvtcW2d8NTdjQ'}]})
                gfile.SetContentFile(file_path)
                gfile.Upload()
            def delete(name):
                file = self._search_in_list(self._default_folder,name)
                if file is not None:
                    file.Delete()
            def download(name):
                file = self._search_in_list(self._default_folder, name)
                if file is not None:
                    file.GetContentFile(file['title'])

            def _read(folder_name = None, asObj = False):
                if folder_name is None:  
                    folder_id = self._default_folder
                else:
                    folder_id = self.folder_crud().id_for_name(folder_name)
                lists = self._drive.ListFile({
                    'q': "'{}' in parents and trashed=false".format(folder_id)
                }).GetList()
                if asObj:
                    return lists
                return [(l['title'], l['id']) for l in lists]

            def isdir(ele):
                return ele['mimeType'] == "application/vnd.google-apps.folder" 
        return Temp

    def id_for_name(self, name):
        folders = name.split("/")
        for fl in folders:
            if first_time:
                folder_id = self._search_in_list(self._default_folder, fl)
                continue
            folder_id = self._search_in_list(folder_id['id'], fl)
        return folder_id['id']


    def _search_in_list(self, folder_id, name):
        lists = self._drive.ListFile({
                'q': "'{}' in parents and trashed=false".format(folder_id)
            }).GetList()
        for val in lists:
            if val['title'] == name:
                return val
        return None