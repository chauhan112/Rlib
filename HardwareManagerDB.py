from SearchSystem import GeneralSearchEngine
class HardwareManagerDB:
    def search():
        class Temp:
            def name():
                return GeneralSearchEngine(content, callBackFunc=lambda key, con: print(con[key]))
            def properties():
                from SearchSystem import GeneralSearchEngine, MultilineStringSearch
                ppr = GeneralSearchEngine(HardwareManagerDB.crud()._load(), 
                          searchFunc=lambda word, con, case, reg: GeneralSearchEngine.tools().iterate(
                              con, 
                              ifFunc = lambda i,key, cont: MultilineStringSearch(cont[key]['property']).pattern(word) is not None
                                  if reg else MultilineStringSearch(cont[key]['property']).wordSearch(word,case) is not None,
                              resAppender = lambda i, key, cont: key

                          ),
                          callBackFunc= lambda key, con: print(con[key]['position']),
                          toolTipFunc= lambda key, con: con[key]['position']
                         )
                return ppr
            
            def position():
                class Temp:
                    def forObjects():
                        from ComparerDB import ComparerDB
                        gg = GeneralSearchEngine(HardwareManagerDB.crud()._load(),  
                                searchFunc = lambda word,cont,case, reg: GeneralSearchEngine.tools().iterate(
                                        cont, ifFunc = lambda i,val, con: ComparerDB.has(word= word, content =con[val]['position'], 
                                                                                         case=case,reg =reg)),
                                callBackFunc= lambda key, con: print(key),
                                buttonNameFunc=lambda key, con: con[key]['position']

                               )
                        return gg
                    
                    def descriptions():
                        pass
                return Temp
        return Temp
    
    def crud():
        from jupyterDB import jupyterDB
        class HardwareObj:
            def __init__(self,name, objValDic):
                self.name = name
                self.attribute = objValDic
                
            def addProperty(self, *properties):
                self.attribute['property'] = list(self.attribute['property'])
                self.attribute['property'] += properties
                self.attribute['property'] = set(self.attribute['property'])
                self._write()
            
            def setPosition(self, newPos):
                self.attribute['position'] = newPos
                self._write()
            
            def _write(self):
                Temp._write().obj(self.name, self.attribute)
            
        class Temp:
            _fileName = "hardwareManager"
            def add(name, properties, position, overwrite = False):
                content = Temp._load()
                if(name in content):
                    raise IOError("Value already exists")
                if(type(properties) == str):
                    properties = set(properties.split(","))
                content[name] = {
                    'property': set(properties),
                    'position':position
                }
                Temp._write().content(content)
            
            def _load():
                return jupyterDB.pickle().read(Temp._fileName)
            
            def _write():
                class Tem:
                    def obj(name , prpty):
                        content = Temp._load()
                        content[name] = prpty
                        Tem.content(content)
                        
                    def content(contents):
                        jupyterDB.pickle().write(contents, Temp._fileName)
                return Tem
            
            def get():
                class T:
                    def asObj(name):
                        content = Temp._load()
                        return HardwareObj(name, content[name])
                    def asDic(name):
                        return Temp._load()[name]
                return T
            def delete(name):
                content = Temp._load()
                del content[name]
                Temp._write().content(content)
        return Temp
    