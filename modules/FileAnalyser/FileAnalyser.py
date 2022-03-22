from OpsDB import IOps
from modules.mobileCode.CmdCommand import GController, IReturnable, IDisplayElements, \
    GCommand, CmdCommandHandler, GParentable
import os
from SerializationDB import SerializationDB
class IFiller:
    def fill(self):
        pass

class IAnalyser:
    def analyse(self):
        pass

class IDataSetable:
    def setData(self, data):
        raise NotImplementedError("abstract method")

class IFileListGetter:
    def getFiles(self):
        pass

class IExplorer:
    def explore(self):
        pass

class GDataSetable(IDataSetable):
    def setData(self, data):
        self.data = data

class GFiller(IFiller, GDataSetable):
    def __init__(self, fileFunc, folderFunc):
        self.fileFunc = fileFunc
        self.folderFunc = folderFunc
        self._metaStr = 'metaData'
        self._dataStr = 'data'

    def fill(self):
        val = self._fill(self.data)
        self.data[self._metaStr] = val
        return self.data

    def _fill(self, dic, loc=[]):
        if dic[self._dataStr] == {}:
            return self.fileFunc(loc)

        vals = []
        for key in dic[self._dataStr]:
            try:
                val = self._fill(dic[self._dataStr][key], loc + [key])
            except Exception as e:
                val = -1
                print(e)
                print(key + " was not being able to read")
                continue
            dic[self._dataStr][key][self._metaStr] = val
            vals.append(val)
        re = self.folderFunc(vals, loc)
        dic[self._metaStr] = re
        return re

class SizeFiller(GFiller):
    def __init__(self):
        super().__init__(self.getSize, self.folderSize)

    def getSize(self, loc):
        path = os.sep.join(loc)
        return os.stat(path).st_size

    def folderSize(self, arr, loc):
        return sum(arr)

class NumberFiller(GFiller):
    def __init__(self):
        super().__init__(lambda x: 1, lambda arr, loc: sum(arr))

class SortDicWithMeta(IOps, GDataSetable):
    def __init__(self, reverse=False):
        self.reverse = reverse
        self._metaStr = 'metaData'

    def execute(self):
        #dic = self.data['data']
        arr = sorted(dic, key=lambda x: self.data[x][self._metaStr],
                     reverse=self.reverse)
        newDic = {'data': {}}
        newDic['metaData'] = self.data['metaData']
        for k in arr:
            newDic['data'][k] = dic[k].copy()
        return newDic

class MetaTheDictionary(IOps, GDataSetable):
    def execute(self):
        return self.metaDic(self.data)

    def metaDic(self, dic):
        if type(dic) != dict:
            return {'metaData': {}, 'data': dic}
        newDic = {}
        newDic['data'] = dic.copy()
        for key in dic:
            newDic['data'][key] = self.metaDic(dic[key])
        newDic['metaData'] = {}
        return newDic

class FileList2Dic(IOps, GDataSetable):
    def __init__(self, sep=None):
        self.sep = sep
        if sep is None:
            self.sep = os.sep
    def execute(self):
        from ListDB import ListDB
        dic = {}
        for f in self.data:
            ListDB.dicOps().addEvenKeyError(dic, f.split(self.sep), {})
        return dic

class AllFilesReader(IFileListGetter, GDataSetable):
    def __init__(self, path="."):
        self.setData(path)

    def getFiles(self):
        from Path import Path
        return Path.getFiles(self.data, True)

class GFileListGetter(IFileListGetter):
    def __init__(self, files):
        self.files = files

    def getFiles(self):
        return self.files

class FromPickle(IFileListGetter, GDataSetable):
    def getFiles(self):
        return SerializationDB.readPickle(self.data)

class ExecuteDatable(IOps):
    def __init__(self, OpClass, data):
        self.cls = OpClass
        self.data = data

    def execute(self):
        ins = self.cls()
        ins.setData(self.data)
        return ins.execute()

class MetaLister(IReturnable, GParentable,GDataSetable):
    def __init__(self):
        self.pos = []
        self._metaStr = 'metaData'
        self.reverse = False

    def get(self):
        content = self.currentValue()['data']
        arr = sorted(content, key=lambda x: content[x][self._metaStr], reverse = self.reverse)
        vals = [content[ke][self._metaStr] for ke in arr]
        return list(zip(arr, vals))

    def currentValue(self):
        from ListDB import ListDB
        loc = []
        for ke in self.pos:
            loc.append('data')
            loc.append(ke)
        content = ListDB.dicOps().get(self.data, loc)
        return content

class MetaDicValSelected:
    def __init__(self, metaLister):
        self.metaLister = metaLister

    def run(self, ele):
        val = ele.getCurrentValue() [0]
        self.metaLister.pos.append(val)

class DisplayFileAnalyser(IDisplayElements, GCommand):
    def __init__(self, idd="l", infoFunc = lambda x: str(x)):
        super().__init__(idd)
        self.infoFunc = infoFunc

    def callback(self):
        elements = self.parent.lister.get()
        content = self.parent.lister.currentValue()
        tsize = content['metaData']
        for i, (name, si) in enumerate(elements):
            if (os.path.isdir(os.sep.join(self.parent.lister.pos + [name]))):
                self.printFormatted('>', i, name, tsize, si)
            else:
                self.printFormatted('|', i, name, tsize, si)

    def printFormatted(self, pre, i, word, tsize, size):
        if tsize == 0:
            tsize = .0001
        from WordDB import WordDB
        forma = WordDB.formatting()
        print(pre + f'{forma.integer(i,3)}. {forma.word(word, 15)}-' + \
              forma.word("|" * int(20 * size / tsize), 20) + self.infoFunc(size))
        
    def getDisplayerCommands(self):
        a = [ Goback('b')]
        [i.setParent(self) for i in a]
        return a

    def getHelp(self):
        return self.id, 'display files distribution'

class Goback(GCommand):
    def callback(self):
        if len(self.parent.parent.lister.pos) > 0:
            self.parent.parent.lister.pos.pop()

    def getHelp(self):
        return self.id, 'go back'

class Save(GCommand):
    def callback(self):
        outfileName = input("output: ")
        SerializationDB.pickleOut(self.parent.parent.lister.data, outfileName)

    def getHelp(self):
        return self.id, 'save current content'

class MetaDicExplorer(IExplorer, GDataSetable):
    def __init__(self):
        lsiter = MetaLister()
        disp = DisplayFileAnalyser("l")
        disp._runAfter = True
        self.cnt =GController(cmdRunner = CmdCommandHandler(callback=MetaDicValSelected(lsiter).run,extraCommands  =[Save('s')]),lister=lsiter,
                         displayer= disp)
                 
        
    def explore(self):
        self.cnt.lister.setData(self.data)
        self.cnt.run()
    
    def setFunc(self, func = lambda x: str(x)):
        self.cnt.elementsDisplayer.infoFunc = func
        
#####################################
    
class FileAnalyser(IAnalyser):
    def __init__(self):
        self.setFileReader(FromPickle())
        self.setFiller(SizeFiller())
        self.setExplorer(MetaDicExplorer())
    def analyse(self):
        files = self.reader.getFiles()
        dic = FileAnalyser.getMetaDicInfo(files, self.filler)
        self.explorer.setData(dic)
        self.explorer.explore()
    def setFileReader(self, reader: IFileListGetter):
        self.reader = reader
    def setFiller(self, filler:IFiller):
        self.filler = filler
    def setPostProcesser(self,pprocess: IOps):
        self.pprocess = pprocess
    def setExplorer(self, exp:IExplorer):
        self.explorer = exp
    
    def analyseFromFile(pklFile, reverse = True):
        data =SerializationDB.readPickle(pklFile)
        exp = MetaDicExplorer()
        exp.cnt.lister.reverse = reverse
        exp.setData(data)
        exp.explore()
        
    def sizeb(si):
        p = lambda x: str(round(x,2))
        if si > 1024*1024* 1024:
            return p(si / 1024**3) + " gb"
        elif si > 1024*1024:
            return p(si / (1024*1024)) + " mb"
        elif si > 1024:
            return p(si/ 1024) + " kb"
        else:
            return p(si) + " bytes"
            
    def getMetaDicInfo(files, filler: IFiller):
        dic = ExecuteDatable(FileList2Dic, files).execute()
        metaDic = ExecuteDatable(MetaTheDictionary, dic).execute()
        filler.setData(metaDic)
        newDic = filler.fill()
        return newDic
        
######

class FileAnalyse:
    def size():
        class Temp:
            def fromPath(path, save = None):
                fa = FileAnalyser()
                fa.explorer.setFunc(FileAnalyser.sizeb)
                afr = AllFilesReader(path)
                fa.setFileReader(afr)
                fa.analyse()
                return fa
    
            def fromPickle(pickle):
                mde  = MetaDicExplorer()
                mde.setFunc(FileAnalyser.sizeb)
                data = SerializationDB.readPickle(pickle)
                mde.setData(data)
                mde.explore()
        return Temp


