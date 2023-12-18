from enum import Enum
FoodCategory = Enum("FoodCategory","available allFoods primary catalyst secondary drinks")
class HealthDB:
    storage_id = "bd619c1f36de48508125b4aedc791e6e"
    def groupCrud():
        pkl = HealthDB._read()
        class Temp:
            loc = 'groups'
            def getAllGroups():
                return FoodCategory.__dict__['_member_names_']
            
            def read(category = FoodCategory.available):
                val = pkl.read([Temp.loc, category.name])
                return val
            
            def add(food, category= FoodCategory.available):
                if(category.name not in pkl.getContent()[Temp.loc]):
                    pkl.add([Temp.loc, category.name], set([]))
                val = Temp.read(category)
                val.add(food)
                pkl.add([Temp.loc, category.name],val, overwrite=True )
                
            def remove(food, category=FoodCategory.available):
                val = Temp.read(category)
                val.remove(food)
                pkl.add([Temp.loc, category.name],val, overwrite=True )
                
        return Temp
    
    def _read():
        from StorageSystem import StorageSystem
        return StorageSystem.dataStructureForIndex(HealthDB.storage_id)
    