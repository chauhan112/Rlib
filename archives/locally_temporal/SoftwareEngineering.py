from SerializationDB import SerializationDB
from LibsDB import LibsDB
from IPython.display import HTML
class SoftwareEngineering:
    def links():
        pass

    def paths():
        pass

    def designs(typ = None):
        pass
    
    def pickle():
        return SerializationDB.readPickle(LibsDB.picklePath("softwareEngineering.pkl"))

    def diagramsType(typ = None):
        if(typ is None):
            return HTML(SoftwareEngineering.pickle()['diagrams type'])
        elif(typ.lower() in ['']):
            pass
    
    def designExamples(typ):
        pass

    def mvcFolderStructureExamples():
        return SoftwareEngineering.pickle()['mvc']