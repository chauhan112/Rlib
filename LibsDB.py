from LibPath import *
import os

class LibsDB:
    def cloudPath():
        from RegexDB import RegexDB
        return RegexDB.regexSearch(".*cloud", getPath())[0].replace("\\",os.sep)
    
    def picklePath(val = None):
        k = os.sep.join([resourcePath(), 'pickle'])
        k = os.path.abspath(k)
        if(val == ''):
            return os.listdir(LibsDB.picklePath())
        if(val is not None):
            k = os.sep.join([k, val])
            if(not val.endswith(".pkl")):
                k += ".pkl"
        return k
    
    def dbPath(val):
        k = os.sep.join([resourcePath(), 'dbs'])
        k = os.path.abspath(k)
        if(val == ''):
            return os.listdir(k)
        if(val is not None):
            k = os.sep.join([k, val])
        return k
    
    def runBasic(opcode = 0, *args):
        """
        # 0 -> get all sections
        # 1 -> get crud operations
        # 2 -> specify keys like 'imports', 'info display' eg: runBasic(2, 'imports' , '..')
        # 3 -> nots runBasic(3,'reminder timer')
        """
        class Temp:
            def display():
                from jupyterDB import jupyterDB
                name = "runBasic"
                k = jupyterDB.pickle().read(name)
                code = ""
                for cat in k:
                    code += f"# {cat}\n{k[cat]}\n\n"
                return jupyterDB.displayer(code)
            
            def crud():
                from PickleCRUDDB import PickleCRUD
                pi = PickleCRUD("runBasic")
                return pi
            
            def _content():
                from SerializationDB import SerializationDB
                k = SerializationDB.readPickle(LibsDB.picklePath("runBasic.pkl"))
                return k
            
            def getText(keys = []):
                k = Temp._content()
                content = ""
                for e in k:
                    if len(keys) != 0:
                        if e in keys:
                            content += k[e] + "\n"
                    else:
                        content += k[e] + "\n"
                return content
            def notKeys( notKeys):
                from AIAlgoDB import AIAlgoDB
                allKeys = list(Temp._content().keys())
                ss =AIAlgoDB.incrementalSearch(allKeys)
                resultingKeys = []
                founds = []
                for ele in notKeys:
                    founds += ss.search(ele)
                for f in founds:
                    if f in founds:
                        allKeys.remove(f)
                return allKeys

        if opcode == 1:
            return Temp
        elif opcode == 2:
            if len(args) == 0:
                return Temp.getText(['imports'])
            return Temp.getText(args)
        elif opcode == 3:
            resultingKeys = Temp.notKeys(args)
            return Temp.getText(resultingKeys)
        return Temp.getText()