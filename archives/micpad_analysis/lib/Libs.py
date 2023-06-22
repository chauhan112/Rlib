import pickle
import gzip
import re
import os
import pyperclip
import matplotlib.pyplot as plt

class Libs:
    def serialize():
        class Temp:
            def pickleOut(dataStructure, outFileName):
                data = pickle.dumps(dataStructure)
                dataCompressed = Temp.compressToBinVal(data)
                with open(outFileName, "wb") as f:
                    f.write(dataCompressed)
            def readPickle(filePath):
                with open(filePath, "rb") as f:
                    binValCompressed = f.read()
                try:
                    binVal = Temp.decompressFromBinVal(binValCompressed)
                except:
                    binVal = binValCompressed
                return pickle.loads(binVal)
            def compressToBinVal(content):
                return gzip.compress(content)
            def decompressFromBinVal(content):
                return gzip.decompress(content)
        return Temp
    def fileOps():
        class Temp:
            def appendToFile(filename, content):
                if(not os.path.exists(filename)):
                    print("File does not exists")
                    return 
                with open(filename, "a") as myfile:
                    myfile.write(content)
            def hasExtension(file, exts):
                if(type(exts) == str):
                    exts = [exts]
                tr = False
                for ext in exts:
                    tr = tr or file.endswith("." + ext) or file.endswith("." + ext.upper())
                return tr
            def openFile(file):
                if(os.path.exists(file)):
                    from sys import platform
                    if platform == "linux" or platform == "linux2":
                        os.system(f"xdg-open '{file}'")
                    else:
                        import webbrowser
                        webbrowser.open(file)
                else:
                    print(file + " does not exists")
            def getFileContent(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    return f.read()
            
            def getSize(files):
                si = 0
                for f in files:
                    si += os.stat(f).st_size
                return str(si / 1024) + " kb"
            
        return Temp
    def clip():
        class Temp:
            def text():
                return pyperclip.paste()
            def copy(content):
                if(type(content) != str):
                    raise IOError("Can only copy string")
                if(os.name == "nt"):
                    pyperclip.copy(content)
                else:
                    os.system("echo '{}' | xclip -selection clipboard".format(content))
        return Temp
    def stringOps():
        class Temp:
            def replaceWithRegex(regex,replacingPart,  text):
                return re.sub(regex, replacingPart, text)
            def tokenize(content):
                return list(set([content[i:j] for i, j in Temp.regSearch('\w+',content)]))
            def regSearch(regex, content):
                matches = re.finditer(regex, content)
                found = []
                for i,match in enumerate(matches):
                    found.append([match.start(),  match.end()])
                return found
        return Temp
    def path():
        class Temp:
            def changeSeparator(path):
                return Libs.stringOps().replaceWithRegex(r"\\+", "<sjdfsdj>", Libs.stringOps().replaceWithRegex("/+","<sjdfsdj>",  
                    path)).replace("<sjdfsdj>", os.sep)
            def filesWithExtensions( extensions ,directory = None, walk = True):
                results = []
                if(directory is None):
                    directory = os.getcwd()
                files = Temp.getFiles(directory, walk)
                for file in files:
                    if(Libs.fileOps().hasExtension(file, extensions)):
                        results.append(file)
                return results
            def getFiles(directory, walk = False):
                if(walk):
                    return Temp.getAllFilesInFolder(directory)
                cand = os.listdir(directory)
                files = []
                for file in cand:
                    if(os.path.isfile(directory + os.sep + file)):
                        files.append(directory + os.sep + file)
                return files
            def getAllFilesInFolder(directory):
                file_paths = []
                for root, directories, files in os.walk(directory):
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        file_paths.append(filepath)
                return file_paths
            def joinPath(*arr):
                return Temp.changeSeparator(os.sep.join(arr))
        return Temp
    def displayTableFromArray(arr, displayIt = True):
        from IPython.display import HTML, display
        arrHtmlTxt = "".join([f"<th>{head}</th>\n  " for head in arr[0]])
        arrHtmlTxt = f"<tr>{arrHtmlTxt}</tr>\n"
        for row in arr[1:]:
            vals = ""
            for val in row:
                vals += f"<td>{val}</td>\n  "
            arrHtmlTxt += f"<tr>{vals}</tr>\n"
        if(displayIt):
            display(HTML(f"<table>{arrHtmlTxt}</table>"))
            return
        return f"<table>{arrHtmlTxt}</table>"
    def barPlotDic(dic, sortDic = False, rotate = 0, xLabel= "", yLabel ="", 
               barLabel = False, filterFunc = lambda x: True, changeFigSize = False):
        dic = {key: dic[key] for key in dic if filterFunc(key)}
        if(sortDic):
            dic = Libs.listOps().sortDicBasedOnValue(dic)
        if(changeFigSize):
            plt.rcParams["figure.figsize"] = (20,10)
        fig, ax = plt.subplots()
        vals = dic.values()
        bar = ax.bar(dic.keys(), vals)
        x = plt.xticks(rotation= rotate)
        plt.xlabel(xLabel, fontsize=18)
        if(barLabel):
            for i, v in enumerate(vals):
                ax.text(i-.25, v, str(v))
        plt.ylabel(yLabel, fontsize=18)
        plt.rcParams["figure.figsize"] = plt.rcParamsDefault["figure.figsize"]
    def listOps():
        class Temp:
            def sortDicBasedOnValue(dic):
                return { k: v for k, v in sorted(dic.items(), key=lambda item: item[1]) }
        return Temp