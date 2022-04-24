import os
from FileDatabase import File
from OpsDB import OpsDB
from SystemInfo import SystemInfo
class GitDB:
    repo = None
    currentBranch = None
    def syntax(keyWord=None):
        from jupyterDB import jupyterDB
        name = "syntax"
        k = jupyterDB.pickle().read(name)
        from Database import Database
        return Database.dbSearch(Database.dicDB(k['git']), keyWord)
        
    def setPath(gitPath):
        from git import Repo
        GitDB.repo = Repo(gitPath)
        GitDB.currentBranch = GitDB.branches().currentBranch()
    def branches():
        class Temp:
            def currentBranch():
                return GitDB.execute("git status").splitlines()[0].replace("On branch ", "")
            def allBranches():
                return [r.name for r in GitDB.repo.references]
            def totalNumberOfBranch():
                return len(Temp.allBranches())
            def selectBranch(name):
                pass
        return Temp
    
    def commits():
        class Temp:
            def totalNumberOfCommits(ref_name = None):
                if(ref_name is None):
                    return len(list(GitDB.repo.iter_commits()))
                return len(Temp.getAllCommits(ref_name).splitlines())
            def getAllCommits(ref_name=None, options ="--oneline", number= ""):
                options += " " + number
                if(ref_name is None):
                    ref_name = GitDB.branches().currentBranch()
                if(ref_name =="master"):
                    return GitDB.execute(f"git log {options} master")
                return GitDB.execute(f"git log {options} master..{ref_name}")
            def changeToCommit(commitHash, force =""):
                if(GitDB.currentBranch is None):
                    GitDB.currentBranch = GitDB.branches().currentBranch()
                GitDB.execute(f"git checkout {force} {commitHash}")           
            def checkoutLatestCommit():
                if(GitDB.currentBranch is not None):
                    Temp.changeToCommit(GitDB.currentBranch)
            def addTag(commit_hash, tag):
                if(GitDB.currentBranch is None):
                    GitDB.currentBranch = GitDB.branches().currentBranch()
                GitDB.execute(f"git tag {tag} {commit_hash}")      
                
        return Temp
        
    def execute(command):
        return GitDB.repo.git().execute(command)
    
    def status():
        print(GitDB.execute("git status"))

    def gitAdd(files, gitFolder="."):
        gitFolder = os.path.abspath(gitFolder)
        volumeLabel = gitFolder[:2]
        for f in files:
            a, b = OpsDB.cmd().run([volumeLabel, f'cd "{gitFolder}"', f'git add "{f}"'], getErr=True)
            print(a+ "\n"+ b)

class GitCompare:
    def __init__(self, filesListA, filesListB):
        self.path = GitCompare.getDicOfFilesPath(filesListA, filesListB)
        
    def getDicOfFilesPath(filesA, filesB):
        if(len(filesA) < len(filesB)):
            rebasedFiles = filesA
            backupFiles = filesB
        else:
            rebasedFiles = filesB
            backupFiles = filesA
            
        a = OpsDB.grouper(os.path.basename, backupFiles)
        b = OpsDB.grouper(os.path.basename, rebasedFiles)
        for key in b:
            b[key].append(a[key][0])
        return b
    
    def fileDiff(filePathA, filePathB):
        contentA = File.getFileContent(filePathA)
        contentB = File.getFileContent(filePathB)
        if(contentA != contentB):
            return os.path.basename(filePathA)
    
    def stringDiff(first,second, multiline = True):
        import difflib
        if(not multiline):
            return list(difflib.unified_diff(first, second))
        for text in difflib.unified_diff(first.split("\n"), second.split("\n")):
            if text[:3] not in ('+++', '---', '@@ '):
                print (text)
        
    def giveNameOfOnlyChangedFiles(self):
        files = []
        i = 1
        for  key in (self.path):
            k = GitCompare.fileDiff(*self.path[key])
            if( k is not None):
                print("{:0>2d}. ".format(i), end="")
                print(k)
                files.append(k)
                i = i+1
        return files

    def getLinesOfChangedFile(self):
        pass
        
class IGitCommand:
    def act(self):
        raise NotImplementedError("abstract method")
    
class ChangedFiles(IGitCommand):
    def __init__(self, path2repo):
        self.path = os.path.abspath(path2repo)
    def act(self):
        from git import Repo
        from Path import Path
        repo = Repo(self.path)
        changedFiles= [ item.a_path for item in repo.index.diff(None) ]
        res = []
        for f in changedFiles:
            file =Path.joinPath(self.path,f)
            if(os.path.exists(file)):
                res.append(file)
        return res

class DeletedFiles(IGitCommand):
    def __init__(self, path2repo):
        self.path = os.path.abspath(path2repo)
        
    def act(self):
        from git import Repo
        repo = Repo(self.path)
        changedFiles= [ item.a_path for item in repo.index.diff(None) ]
        res = []
        for f in changedFiles:
            file =Path.joinPath(self.path,f)
            if(not os.path.exists(file)):
                res.append(file)
        return res
    
class UntrackedFiles(IGitCommand):
    def __init__(self, path2repo):
        self.path = os.path.abspath(path2repo)
    def act(self):
        from git import Repo
        from Path import Path
        repo = Repo(self.path)
        return [Path.joinPath(self.path,f) for f in repo.untracked_files]

class RepoName(IGitCommand):
    def __init__(self,path2repo):
        self.path = os.path.abspath(path2repo)
    def act(self):
        from git import Repo
        repo = Repo(self.path)
        return repo.remotes.origin.url.split('.git')[0].split('/')[-1]

class IGitPush:
    def push(self, commit_msg="something"):
        raise NotImplementedError("abstract method")

class GithubApiPush(IGitPush):
    def __init__(self, username, password, path2repo):
        self.username = username
        self.password = password
        self.path = path2repo
    
    def push(self, commit_msg= "time"):
        import base64
        from github import Github
        from github import InputGitTreeElement
        
        files2push = ChangedFiles(self.path).act() + UntrackedFiles(self.path).act()
        g = Github(self.username,self.password)
        repo = g.get_user().get_repo(RepoName(self.path).act()) 
        master_ref = repo.get_git_ref('heads/master')
        master_sha = master_ref.object.sha
        base_tree = repo.get_git_tree(master_sha)

        element_list = list()
        for i, entry in enumerate(files2push):
            with open(entry) as input_file:
                data = input_file.read()
            if entry.endswith('.png'): # images must be encoded
                data = base64.b64encode(data)
            element = InputGitTreeElement(entry.replace(self.path, "").strip(os.sep).replace(os.sep, "/"), '100644', 'blob', data)
            element_list.append(element)

        tree = repo.create_git_tree(element_list, base_tree)
        parent = repo.get_git_commit(master_sha)
        commit = repo.create_git_commit(commit_msg, tree, [parent])
        master_ref.edit(commit.sha)
        return tree.tree

class CommandLinePush(IGitPush):
    def __init__(self, username, password, path2repo):
        self.username = username
        self.password = password
        self.path = path2repo
        
    def push(self, commit_msg="something"):
        steps = [
             f'cd "{self.path}"', 
             "git config --global core.longpaths true", 
             'git config --global user.email "rajababuchauhan500@gmail.com"', 
             f'git config --global user.name "{self.username}"', 
             'git stash',
             'git pull --all',
             'git stash pop',
             'git add .',  
             f'git commit -m "{commit_msg}"', 
             f'git push https://{self.password}@github.com/{self.username}/{RepoName(self.path).act()} -f',
             'git pull'
        ]
        return GRunGitCommand(self.path, steps).act()

class GitPush(IGitCommand):
    def __init__(self, pushForm: IGitPush):
        self.pushMethod = pushForm
    def act(self):
        self.pushMethod.push()

class GitSSHPush(IGitPush):
    def __init__(self, path2repo):
        self.path = path2repo
    
    def push(self, commit_msg = None):
        if commit_msg is None:
            from LibPath import computerName
            commit_msg = computerName()
        steps = [f'cd "{self.path}"','git add .', f'git commit -m"{commit_msg}"', "git push"]
        return GRunGitCommand(self.path, steps).act()

class IGitPull:
    def pull(self):
        raise NotImplementedError("abstract method")

class GitSSHPull(IGitPull):
    def __init__(self, path2repo):
        self.path = path2repo
    def pull(self):
        steps = [f'cd "{self.path}"', 'git pull']
        return GRunGitCommand(self.path, steps).act()

class GitStatus(IGitCommand):
    def __init__(self, path2repo):
        self.path = path2repo
    def act(self):
        steps = [f'cd "{self.path}"', 'git status']
        return GRunGitCommand(self.path, steps).act()
        
class GitPull(IGitCommand):
    def __init__(self, path2repo, username):
        self.path = path2repo
        self.username =username
        
    def act(self):
        steps = [
             f'cd "{self.path}"', 
             "git config --global core.longpaths true", 
             'git config --global user.email "rajababuchauhan500@gmail.com"', 
             f'git config --global user.name "{self.username}"', 
             'git pull --all'
        ]
        return GRunGitCommand(self.path, steps).act()

class GRunGitCommand(IGitCommand):
    def __init__(self, path2repo, steps):
        self.path = os.path.abspath(path2repo)
        self.steps = steps
    def act(self):
        if(not SystemInfo.isLinux()):
            self.steps = [f'{self.path[:2]}' ] +  self.steps
        a, err = OpsDB.cmd().run(self.steps, getErr=True)
        out = a + '\n' + err
        print(out)
        return out