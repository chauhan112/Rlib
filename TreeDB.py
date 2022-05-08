import os,yaml
from ClipboardDB import ClipboardDB
from Path import Path
from FileDatabase import File
from SerializationDB import SerializationDB
from LibsDB import LibsDB
from SearchSystem import SearchEngine, DicSearch
import urllib
import webbrowser

class TreeDB:
    def decodeContent(content = ''):
        if(content == ''):
            content = ClipboardDB.getText()
        from ModuleDB import ModuleDB
        from htmlDB import htmlDB

        class Temp:
            def __init__(self, content ):
                self._content = urllib.parse.unquote(content)
                self._soup = htmlDB.getParsedData(self._content, "xml")
            def soup(self):
                return self._soup
            def text(self):
                return htmlDB.htmlDecode(self._soup.prettify())
            def display(self):
                from IPython.display import display
                display(ModuleDB.colorPrint("html", self.text()))
            def originalText(self):
                return self._content
            def soup_without_xml_part(self):
                return htmlDB.getParsedData(self._content)
            def quote(self, content):
                return urllib.parse.quote(content).replace("/", "%2F").replace("%28" , "(" ).replace("%29", ")")
            

        tem = Temp(content)
        return tem

    def openWebLink(link):
        from LibPath import computerName
        if (computerName() == "mobileTermux"):
            os.system(f'termux-open-url "{link}"')
        else:
            webbrowser.open(link)

    def drawioPages(filePath):
        from WordDB import WordDB
        from RegexDB import RegexDB
        from CompressDB import CompressDB
        content = File.getFileContent(filePath)
        beginRanges = WordDB.searchWordWithRegex("<diagram .*?>", content)
        endRanges = WordDB.searchWordWithRegex("</diagram>", content)
        res = {}
        for (a,b), (c,_) in zip(beginRanges, endRanges):
            res[RegexDB.regexSearch('id=".*"',content[a:b])[0]] = TreeDB.decodeContent(
                CompressDB.content().decode_base64_and_inflate(content[b:c])).text()
        return res

    def forest():
        class Temp:
            def getTrees():
                class Tem:
                    def asDic():
                        class Te:
                            def loc():
                                forestPath = Temp.path()
                                files = Path.filesWithExtension("drawio", forestPath)
                                dic = {f.replace(forestPath, "").strip(os.sep): f for f in files}
                                return dic

                            def basename():
                                dic = Te.loc()
                                newDic = {os.path.basename(key): dic[key] for key in dic}
                                return newDic
                        return Te
                    def asList():
                        return Path.filesWithExtension("drawio", Temp.path())
                    def oneFile(name):
                        if(not name.endswith(".drawio")):
                            name += ".drawio"
                        return Tem.asDic().basename()[name]
                return Tem
            def path():
                return ForestDB.getForestPath()
            def search(word, reg = False):
                from Database import D1Database
                from WidgetsDB import WidgetsDB
                trees = SerializationDB.readPickle(LibsDB.picklePath("abstraction"))
                vals = list(trees.keys())
                db = D1Database(vals)
                k = [vals[x] for x in db.search(word, reg = reg)]
                def copy(x):
                    ClipboardDB.copy2clipboard(trees[x.description])
                return WidgetsDB.getGrid(7, [WidgetsDB.button(name=x, callbackFunc=copy, tooltip=x) for x in k])
            def cache():
                class Tools:
                    def getAllWordInXml(xmlString):
                        from RegexDB import RegexDB
                        tmp = list(map(lambda x: RegexDB.regexSearch(RegexDB.lookAheadAndBehind(">", "</", ".*"),x)[0],
                            RegexDB.regexSearch("<span .*?</span>", xmlString)))
                        tmp += RegexDB.regexSearch(RegexDB.lookAheadAndBehind('value="', '"', ".*?"), xmlString)
                        tmp = list(set(tmp))
                        return [val.replace("&nbsp;", " ").replace("<br>", "\n") for val in tmp]

                files = Path.filesWithExtension("drawio", Temp.path())
                parsedDic = {}
                for path in files:
                    p = TreeDB.drawioPages(path)
                    parsedDic[path] = {}
                    for page in p:
                        parsedDic[path][page] = Tools.getAllWordInXml(p[page])
                SerializationDB.pickleOut(parsedDic, Path.joinPath(Temp.path(), "searchCached.pkl"))
            def opener(key):
                from AIAlgoDB import AIAlgoDB
                from SearchSystem import GSearch
                files = Path.filesWithExtension("drawio", TreeDB.forest().path())
                files = {os.path.basename(f)[:-1*len(".drawio")].lower(): f for f in files}
                founds = AIAlgoDB.incrementalSearch(files.keys()).search(key)
                if(len(founds) == 0):
                    founds = GSearch._default(key, files.keys())
                if(len(founds) == 0):
                    found = "index"
                else:
                    found = founds[0]

                path = files[found]
                File.openFile(path)
            def ops():
                class Temp:
                    def add(self, name,overwrite = False):
                        pickleFile = 'abstraction'
                        k = SerializationDB.readPickle(LibsDB.picklePath(pickleFile))
                        if(name in k and not overwrite):
                            raise IOError("Name already exits")
                        content = ClipboardDB.getText()
                        k[name] = content
                        SerializationDB.pickleOut(k, LibsDB.picklePath(pickleFile))
                        print("Total number of trees in the forest : " + str(len(k)))
                        print("Content size : " + str(len(content)))

                    def updateKey(self, oldname, newName):
                        con = self._reader()
                        con[newName] = con.pop(oldname)
                        self._writer(con)
                    def _writer(self, k):
                        pickleFile = 'abstraction'
                        SerializationDB.pickleOut(k, LibsDB.picklePath(pickleFile))
                    def _reader(self):
                        pickleFile = 'abstraction'
                        k = SerializationDB.readPickle(LibsDB.picklePath(pickleFile))
                        return k
                return Temp()
        return Temp

    def explorer(content):
        pass
class ForestDB:
    def getForestPath():
        import socket
        computers = {
            'Raja': r"G:\My Drive\Forest",
            'acnbrc': r"C:\Users\rajac\Google Drive\Forest",
            'raja-ZenBook-UX433FN-UX433FN': '/home/raja/GDrive/Forest'
        }
        return computers[socket.gethostname()]

    def search(word, case =True,  reg = False):
        from ComparerDB import ComparerDB
        from RegexDB import RegexDB
        from WidgetsDB import WidgetsDB
        re = SerializationDB.readPickle(Path.joinPath(ForestDB.getForestPath(), "searchCached.pkl"))
        founds = []
        for file in re:
            for page in re[file]:
                if(ComparerDB.has(word ," ".join(re[file][page]), case= False, reg =reg)):
                    founds.append((file, page))
                    break

        pathConverter = lambda p: p.replace(RegexDB.regexSearch(".*?Forest", p)[0],ForestDB.getForestPath())
        names = [(os.path.basename(x).split(".")[0],
                    lambda n, x=x: File.openFile(file=pathConverter(x)),
                    RegexDB.regexSearch(RegexDB.lookAheadAndBehind("name=\"", '"', ".*"), y)[0]
                 ) for x,y in founds]
        widgt = [WidgetsDB.button(x, y, z) for x, y, z in names]
        return WidgetsDB.getGrid(7, widgt)

class TreeCRUD:
    def waterFall(small = 1, copy = 1):
        key = "big waterfall"
        if(small):
            key = "small waterfall"
        manger = TreeCRUD._replaceWithTimeStamp(key)
        if(not copy):
            return manger
        ClipboardDB.copy2clipboard(manger)

    def _replaceWithTimeStamp(key):
        manger = TreeCRUD.getObj(key)
        return TreeCRUD._replaceTimeStamp(manger)

    def _replaceTimeStamp(content, deltaDay = 0):
        from TimeDB import TimeDB
        from htmlDB import htmlDB
        import re
        return re.sub('(Sun|Mon|Tues|Wednes|Thurs|Fri|Satur)day%2C%20\\d+\\.\\d+\\.\\d+',
            htmlDB.urlEncode(TimeDB.getTimeStamp(deltaDay)), content)

    def addObject(key, val):
        content = TreeCRUD._loadOps()
        content[key] = val
        SerializationDB.pickleOut(content, TreeCRUD.getPicklePath())

    def _loadOps():
        file = TreeCRUD.getPicklePath()
        return SerializationDB.readPickle(file)

    def delete(key):
        content = TreeCRUD._loadOps()
        del content[key]
        SerializationDB.pickleOut(content, TreeCRUD.getPicklePath())

    def getPicklePath():
        return LibsDB.picklePath("TreeCRUD")

    def textWithBlueBackground(txt = 'txt'):
        from htmlDB import htmlDB
        from ClipboardDB import ClipboardDB
        ClipboardDB.copy2clipboard(TreeCRUD._loadOps()['text'].replace(htmlDB.urlEncode("{}"), txt))

    def getObj(key):
        return TreeCRUD._loadOps()[key]

    def copyDB(word = None):
        from Database import Database
        from ClipboardDB import ClipboardDB
        content = SerializationDB.readPickle(TreeCRUD.getPicklePath())
        def f(x):
            ClipboardDB.copy2clipboard(x)
            print("copied")
        db = Database.dicDB(content, displayer=f)
        if(word is not None):
            db.search(word)
        return db
    def code_content(content, encode=True):
        from htmlDB import htmlDB
        if encode:
            return htmlDB.urlEncode(content)
        return htmlDB.urlDecode(content)
class TreeSearch(DicSearch):
    def search(self, word,case =False, reg = False):
        return self.key(word, case, reg)

class TreeSearchEngine(SearchEngine):
    def __init__(self, content):
        super().__init__(content, TreeSearch)

    def callback(self , key):
        val = self.searchSys.container[key.description]
        val = TreeCRUD._replaceTimeStamp(val)
        ClipboardDB.copy2clipboard(val)



from OpsDB import IOps
from modules.mobileCode.CmdCommand import GDataSetable

class IElement:
    def name(self):
        raise NotImplementedError("abstract method")
    def priority_value(self):
        raise NotImplementedError("abstract method")

class Node(IElement):
    def __init__(self, name, val):
        self._name= name
        self._val = val
    def name(self):
        return self._name
    def priority_value(self):
        return self._val
class DirNode(IElement):
    def __init__(self, nodes):
        self.nodes = nodes
    def name(self):
        return '_'.join([a.name()[:3] for a in self.nodes])
    def priority_value(self):
        return sum([a.priority_value() for a in self.nodes])

class Priority_tree(IOps, GDataSetable):
    def execute(self):
        data = self.data
        if isinstance(data[0], tuple):
            data = Priority_tree.from_tuple(data)
        tree = self.priority_tree(data)[0]
        return self.tree2dic(tree)

    def from_tuple(list_with_val_weights):
        return [(Node(a, b)) for a, b in list_with_val_weights]

    def priority_tree(self, list_with_weights: list[IElement]):
        if len(list_with_weights) < 2:
            return list_with_weights
        srt = sorted(list_with_weights, key=lambda x: x.priority_value(), reverse=True)
        a = srt.pop()
        b = srt.pop()
        cm = DirNode([a, b])
        srt.append(cm)
        return self.priority_tree(srt)

    def tree2dic(self, nodeTree, res={}):
        if isinstance(nodeTree, DirNode):
            nodes = nodeTree.nodes
            nodes.reverse()
            for node in nodes:
                res[node.name()] = {}
                self.tree2dic(node, res[node.name()])
        else:
            res['val'] = nodeTree.priority_value()
        return res
