from modules.DataServer.Interfaces import INode, IFilePortal, NameContact, IContact
from modules.DataServer.Portals import PathPortal
from modules.DataServer.FileObserve import WatchDogFileObserve, MutuallyExclusiveEventModel
from CryptsDB import CryptsDB
from Path import Path
import os, time
from TimeDB import TimeDB

class Tools:
    def generate_time_id():
        return time.time()
    def moveOrOverrideFile(path, toPath):
        os.system(f'mv -f "{path}", "{toPath}"')
    def combinedName(time:float, basename:str):
        return str(time)+'_'+basename
    def create_dir_if_not_exists(dirpath):
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
class SyncNode(INode):
    def __init__(self, server_path, portal : IFilePortal, interval =1):
        self.portal = portal
        self.path = server_path
        self._tempfolder = self.path + os.sep + '.temp'
        Tools.create_dir_if_not_exists(self._tempfolder)
        self._init2()
        self.interval = interval
    def _init2(self):
        # perform pre processing here
        pass
    def _prefix_path(self, path):
        return self.path + "/" + path
    
    def start(self):
        self.timer = TimeDB.setTimer().regularlyUpdateTime(self.interval, self.run)

class CloudServer(SyncNode):
    def _init2(self):
        self._id = NameContact('server')

    def run(self):
        msg =self.portal.receiveMessage(self._id)
        print(msg)
        for msg_with_time in msg:
            self._process_message(msg_with_time)

    def _process_message(self, msg_with_time):
        print(msg_with_time)
        for time in msg_with_time:
            msg = msg_with_time[time]
            for file in msg:
                self._process_ops(file, msg[file])

    def _process_ops(self, path, info):
        tpath = self._prefix_path(path)
        if info['type'] == 'moved':
            try:
                os.rename(tpath, self._prefix_path(info['destination']))
            except Exception as e:
                print(e)
        elif info['type'] in ['created', 'modified']:
            if info['is_dir']:
                if not os.path.exists(tpath):
                    os.makedirs(tpath)
            else:
                dirname = self._prefix_path(os.path.dirname(path)).strip('/')
                basename = os.path.basename(path)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                dPath = self._download_file(Tools.combinedName(info['time'], basename))
                downloaded_renamed = os.path.dirname(dPath)+"/"+basename
                if os.path.exists(downloaded_renamed):
                    os.remove(downloaded_renamed)
                os.rename(dPath, downloaded_renamed)
                Path.move().files([downloaded_renamed], tpath)

        elif info['type'] == 'deleted':
            os.system(f'rm -rf "{tpath}"')
        else:
            print("unknown operation")

    def stop(self):
        self.timer.cancel()

    def _download_file(self, filename_hint):
        allFiles = self.portal.receiveFile(self._id)
        files = list(filter(lambda x: filename_hint in x, allFiles))
        if len(files) == 1:
            Tools.create_dir_if_not_exists(self._tempfolder)
            self.portal.download(files, self._tempfolder)
            self.portal.deleteFiles(files)
            return self._tempfolder + os.sep + os.path.basename(files[0])
    
class CloudClient(SyncNode):
    def _init2(self):
        meem = MutuallyExclusiveEventModel()
        meem.setData(self.path)
        self.file_observer = WatchDogFileObserve(self.path, model= meem)
        self.server = NameContact("server")
    def start(self):
        super().start()
        self.file_observer.start()
    def run(self):
        changes = self.file_observer.get()
        if len(changes) != 0:
            for path in changes:
                info = changes[path]
                if info['type'] in ['modified', 'created'] and not info['is_dir']:
                    self.portal.sendFile(self._prefix_path(path), self.server,
                        target_name=Tools.combinedName(changes[path]['time'], os.path.basename(path)))
            self.portal.sendMessage(changes, self.server)

    def stop(self):
        self.file_observer.stop()
        self.timer.cancel()

    def upload(self, files, server_loc = None):
        pass

class FileSendablePathPortal(PathPortal, IFilePortal):
    def sendFile(self, filepath, to:IContact, loc = '.', target_name= ""):
        path2contact = self._path(to, loc)
        if not os.path.exists(path2contact):
            os.makedirs(path2contact)
        Path.copyFiles([filepath], path2contact)
        if target_name != "":
            os.rename(path2contact+ os.sep + os.path.basename(filepath),
                path2contact+ os.sep + target_name)

    def receiveFile(self, fromC: IContact,loc = '.'):
        path2contact = self._path(fromC, loc)
        return Path.getFiles(path2contact, True)

    def _path(self, cont: IContact, loc):
        path2contact = self.getPath(cont.getId())
        if loc != '.':
            path2contact = self.getPath(cont.getId(),'files', loc)
        return path2contact

    def download(self, files, local_toP_path):
        Path.copyFiles(files, local_toP_path)

    def deleteFiles(self, files):
        Path.delete(files)


from modules.DataServer.Git import GitSSHManager
from modules.DataServer.Interfaces import IFilePortal, IContact, GPortal
from git import Repo

class GitHubFileSendablePortal(GPortal,IFilePortal):
    def __init__(self, repo_path, ssh_link= None):
        self.path = repo_path
        Tools.create_dir_if_not_exists(repo_path)
        self.repo_name = None
        if ssh_link is not None:
            self.clone(ssh_link)
        self.filePathPortal = FileSendablePathPortal(self.path)
        self.gitManager = GitSSHManager(self.path)
        self._repo = Repo(self.path)
        self._tempchanges = []
        
    def clone(self, link):
        name = os.path.basename(link)
        self.repo_name = name.replace(".git", "")
        if not os.path.exists(self.path + os.sep + self.repo_name):
            print("cloning")
            cwd = os.getcwd()
            os.chdir(self.path)
            os.system(f'git clone {link}')
            os.chdir(cwd)
        self.path += os.sep + self.repo_name
        
    def sendFile(self, filepath, to:IContact, loc = ".", target_name = ""):
        self.gitManager.pull()
        self.filePathPortal.sendFile(filepath, to, loc, target_name)
        print(self._repo.index.diff(None))
        self.push()
        
    def receiveFile(self, fromC: IContact):
        self.gitManager.pull()
        self.filePathPortal.receiveFile(fromC)
        return self.filePathPortal.receiveFile(fromC)
        
    def download(self, files, local_toP_path):
        self.gitManager.pull()
        self.filePathPortal.download(files, local_toP_path)
                
    def deleteFiles(self, files):
        self.gitManager.pull()
        self.filePathPortal.deleteFiles(files)
        print(self._repo.index.diff(None))
        self.push()

    def push(self):
        if len(self._tempchanges) != 0:
            print(self.path, "is pushing")
            self.gitManager.push()
    def sendMessage(self, data, to: IContact):
        self.gitManager.pull()
        self.filePathPortal.sendMessage(data, to)
        print(self._repo.index.diff(None))
        self.push()
    def receiveMessage(self, fromC: IContact):
        self.gitManager.pull()
        return self.filePathPortal.receiveMessage(fromC)

class GoogleFileSendablePortal(GPortal,IFilePortal):
    pass