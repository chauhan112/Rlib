class UbuntuDB:
    def commands():
        from SearchSystem import DicSearchEngine
        from jupyterDB import jupyterDB
        from Database import Database
        from ListDB import ListDB
        from ConformationDB import Confirmation

        class Temp(DicSearchEngine):
            def _callback(self, item):
                print(self.searchSys.container[item])

        class Ops:
            name = 'globals'
            def getKeys():
                keys = list(Ops._getData()['ubuntu'].keys())
                return keys
            
            def _getData():
                return jupyterDB.pickle().read(Ops.name)

            def addNew(key, val, cat = 'commands'):
                k = Ops._getData()
                if(cat not in k['ubuntu']):
                    if(ConformationDB.doUWantToContinue(f'{cat} does not exist. Do you want to add a new category?')):
                        k['ubuntu'][cat] = {}
                k['ubuntu'][cat][key] = val
                jupyterDB.pickle().write(k, Ops.name)

            def search(word = None):
                return Database.dbSearch(Temp(ListDB.dicOps().flatten(Ops._getData()['ubuntu'])), word)

            def delete(key,cat = "commands"):
                k = Ops._getData()
                if(key in k['ubuntu'][cat]):
                    if(ConformationDB.doUWantToContinue(f"Do you want to delete {key} of {cat}?")):
                        del k['ubuntu'][cat][key]
                jupyterDB.pickle().write(k, Ops.name)
        return Ops

    def startUpOps():
        pass