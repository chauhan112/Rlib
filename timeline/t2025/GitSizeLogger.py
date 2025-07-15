from basic import Main as ObjMaker
import os
from git import Repo, GitCommandError
def GitFunctionality():
    k = ""
    def executeFuncs(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return True
            except Exception as e:
                print(f"Error : {e}")
                return False
        return wrapper
    @executeFuncs
    def set_repo_path(repo_url, local_path):
        if os.path.exists(local_path):
            s.handlers.set_path(local_path)
        else:
            s.process.repo = Repo.clone_from(repo_url, local_path)
        s.process.local_path = local_path
        s.process.repo_url = repo_url
    def set_path(path):
        if os.path.exists(path):
            s.process.repo = Repo(path)
            s.handlers.gitpull()
        else:
            raise IOError("path does not exist")
        s.process.local_path = path
    @executeFuncs
    def gitpull():
        repo = s.process.repo
        origin = repo.remotes.origin
        current_branch = repo.active_branch.name 
        print(f"Pulling latest changes from origin/{current_branch}...")
        origin.pull(current_branch)
    @executeFuncs
    def addFiles(files):
        s.process.repo.index.add(files)
    @executeFuncs
    def commit(msg):
        s.process.repo.index.commit(msg)
    @executeFuncs
    def push():
        origin = s.process.repo.remotes.origin
        origin.push()
    s = ObjMaker.variablesAndFunction(locals())
    return s

## WIP
REPO_URL = "git@github.com:chauhan112/JSlib.git" 
LOCAL_REPO_PATH = r"C:\Users\rajab\Desktop\stuffs\global\automated\fileLib\jslib"

def libSize():
    files = Path._filesWithExtensions(["ts", "js", "tsx", "jsx", "css"], LOCAL_REPO_PATH)
    si = Path.getSize(files)
    def compare(timeA, timeB):
        a, b = conv(timeA), conv(timeB)
        delta = abs(a -b)
        return delta
    def conv(timeStr):
        a, b, c= timeStr.split()
        d, m, y = list(map(int, b.split(".")))
        h, mi, se = list(map(int, c.split(":")))
        t = (y*365 + m* 31 + d) * 24* 60 * 60  + h * 60*60 + mi * 60 + se
        return t
    from TimeDB import TimeDB
    timeStamp = TimeDB.getTimeStamp() + " " +  ":".join([str(i) for i in TimeDB.today()[1]])
    k = jupyterDB.pickle().read("logs")
    if compare(k['libSize'][-1][0], timeStamp) > 6*60*60:
        k['libSize'] += [(timeStamp, si)]
        jupyterDB.pickle().write(k, 'logs')

        return f"{s} {size_name[i]}"
    totalSizeInBytes = sum(map(File.size, pyFiles))
    print(convert_size(totalSizeInBytes), "==", round(totalSizeInBytes/1024, 2), "kb")