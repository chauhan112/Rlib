class StuffDB:
    storageID = "a5d1718c84594634a87ec32da17a984a"
    def add(name, location="", properties= [], usecases=[], misc={}):
        from useful.CryptsDB import CryptsDB
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
from modules.Explorer.personalizedWidgets import GenerateNRowsBox, SearchWidget
import ipywidgets as widgets
class IStuffOps:
    def display(self):
        pass
class StuffManager:
    def set_parent(self, parent):
        self._parent = parent
class SearchStuff(IStuffOps, StuffManager):
    def __init__(self):
        self._sw = SearchWidget()
        self._db = NestedDicSearchEngine()
        self._db.set_callback_func(self._default_on_element_click)
        self._out = widgets.Output()
        self._sw.set_database(self._db)
        self._layout = widgets.VBox([self._sw.get(), self._out])
    def display(self):
        self._db.set_container(self._parent._pcrud.getContent())
        display(self._layout)
    def set_res_btn_click_func(self, func):
        self._elements_clicked_func = func
    def _default_on_element_click(self, info):
        self._out.clear_output()
        with self._out:
            self._print_element_info(info)
    def _print_element_info(self, element):
        key, _ = element
        content = self._parent._pcrud.read(key[0])
        print(key[0])
        print("---------")
        print("Location: ", content['location'])
        print('info')
        print("-"*10)
        print(content['info'])
class UpdateStuff(IStuffOps, StuffManager):
    def __init__(self):
        pass
    def display(self):
        pass
class DeleteStuff(IStuffOps, StuffManager):
    def __init__(self):
        pass
    def display(self):
        pass
class ElementContentWidget:
    def __init__(self):
        self._title = widgets.Text(description="name")
        self._location= widgets.Text(description='location')
        self._extra_info = widgets.Textarea(description="extra info", placeholder="data as dictionary or string")
        self._add_btn = widgets.Button(description="add")
        self._layout = widgets.VBox([self._title, self._location, self._extra_info, self._add_btn])
class AddNewStuff(IStuffOps, StuffManager):
    def __init__(self):
        self._ecw = ElementContentWidget()
        self._ecw._add_btn.on_click(self._on_add_click)
    def display(self):
        display(self._ecw._layout)
    def _on_add_click(self, btn):
        print(btn)
class StuffsDB:
    def __init__(self):
        self._pcrud = PickleCRUD("stuffs")
        self._ops = {
            'read': SearchStuff(),
            'add': AddNewStuff(),
            'delete': DeleteStuff(),
            'update': UpdateStuff()
        }
        for v in self._ops.values():
            v.set_parent(self)
        self._layout = None
    def search(self, word, case=False, reg=False):
        pass
    def gui(self):
        if self._gnrb is None:
            self._make_gui()
        return self._gnrb.get()
    def _make_gui(self):
        gnrb = GenerateNRowsBox(3)
        gnrb.get()
        gnrb.get_child(0).add_widget(widgets.Dropdown(options=list(stuffs._ops.keys()), description="ops"))
        btn = widgets.Button(description="select")
        gnrb.get_child(0).add_widget(btn)
        self._out = widgets.Output()
        gnrb.get_child(1).add_widget(self._out)
        btn.on_click(self._on_selected)
        self._gnrb = gnrb
    def _on_selected(btn):
        self._out.clear_output()
        selected_ops = self._gnrb.get_child(0).get_child(0).value
        with self._out:
            self._ops[selected_ops].display()