from enum import Enum
ClothStatus = Enum("ClothStatus","washed unwashed")

class ClothesDB:
    storageID = "e22b70edc6ce4879b98c0d44f47cc85a"
    loc = "clothes"
    def add(name, location="", status= ClothStatus.washed, usecaseTime=[], misc={}):
        from useful.CryptsDB import CryptsDB
        uuid = CryptsDB.generateUniqueId()
        pkl = ClothesDB._read()
        pkl.add([ClothesDB.loc,uuid], {'name':name,'location':location, 'status':status.name, 
                                  'occasions': usecaseTime, 'misc':misc})
        
    def attrCrud(stuff_id):
        pkl = StuffDB._read()
        val = pkl.read([ClothesDB.loc, stuff_id])
        class ListOps:
            def __init__(self, key):
                self.key = key
            def add(self, item):
                val[self.key].append(item)
                pkl.add([ClothesDB.loc,stuff_id], val, True)
                
            def delete(self, item):
                val[self.key].remove(item)
                pkl.add([ClothesDB.loc,stuff_id], val, True)
            
        class Temp:
            def changeName(newName):
                Temp._updateVal({"name":newName})
                
            def updateLocation(newLocation):
                Temp._updateVal({'location':newLocation})
            
            def _updateVal(dic):
                val.update(dic)
                pkl.add([ClothesDB.loc,stuff_id], val, True)
            
            def occasions():
                return ListOps("occasions")
            
            def updateMisc(newMisc):
                val['misc'].update( newMisc )
                pkl.add([ClothesDB.loc,stuff_id], val, True)
                
        return Temp
    
    def removeCloth(stuff_id):
        pkl = StuffDB._read()
        pkl.delete([ClothesDB.loc,stuff_id])
    
    def stuff(id_):
        pkl = StuffDB._read()
        val = pkl.read([ClothesDB.loc, id_])
        class Tem:
            def loc():
                return val['location']
            def name():
                return val['name']
            def occasions():
                return val['occasions']
            def misc():
                return val['misc']
            def allContent():
                return val
        return Tem
    
    def search():
        from useful.SearchSystem import DicSearchEngine
        pkl = StuffDB._read()
        content = pkl.getContent()[ClothesDB.loc]
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
        from useful.StorageSystem import StorageSystem
        return StorageSystem.dataStructureForIndex(ClothesDB.storageID)