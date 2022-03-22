class StuffDB:
    storageID = "a5d1718c84594634a87ec32da17a984a"
    def add(name, location="", properties= [], usecases=[], misc={}):
        from CryptsDB import CryptsDB
        uuid = CryptsDB.generateUniqueId()
        pkl = StuffDB._read()
        pkl.add(["stuffs",uuid], {'name':name,'location':location, 'usecases':usecases, 
                                  'properties': properties, 'misc':misc})

    def attrCrud(stuff_id):
        pkl = StuffDB._read()
        val = pkl.read(["stuffs", stuff_id])
        class ListOps:
            def __init__(self, key):
                self.key = key
            def add(self, item):
                val[self.key].append(item)
                pkl.add(["stuffs",stuff_id], val, True)

            def delete(self, item):
                val[self.key].remove(item)
                pkl.add(["stuffs",stuff_id], val, True)

        class Temp:
            def changeName(newName):
                Temp.updateVal({"name":newName})

            def updateLocation(newLocation):
                Temp.updateVal({'location':newLocation})

            def updateVal(dic):
                val.update(dic)
                pkl.add(["stuffs",stuff_id], val, True)

            def usecases():
                return ListOps("usecases")

            def properties():
                return ListOps("properties")

            def updateMisc(newMisc):
                val['misc'].update( newMisc )
                pkl.add(["stuffs",stuff_id], val, True)

        return Temp

    def removeStuff(stuff_id):
        pkl = StuffDB._read()
        pkl.delete(["stuffs",stuff_id])

    def stuff(id_):
        pkl = StuffDB._read()
        val = pkl.read(['stuffs', id_])
        class Tem:
            def loc():
                return val['location']
            def name():
                return val['name']
            def usecases():
                return val['usecases']
            def properties():
                return val['properties']
            def misc():
                return val['misc']
            def allContent():
                return val
        return Tem

    def search():
        from SearchSystem import DicSearchEngine
        pkl = StuffDB._read()
        content = pkl.getContent()['stuffs']
        class Temp:
            def inNames():
                return DicSearchEngine(Temp._vals("name"))
            def atLoc():
                return DicSearchEngine(Temp._vals("location"))
            def withProperties():
                pass
            def forUsecase():
                pass
            def misc(searchingFunc):
                pass

            def _vals(prpty):
                dic = {}
                for key in content:
                    dic[key] = content[key][prpty]
                return dic

        return Temp

    def _read():
        from StorageSystem import StorageSystem
        return StorageSystem.dataStructureForIndex(StuffDB.storageID)