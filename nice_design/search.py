class Main:
    def textSearch(reg, container):
        ts =TextSearch()
        grc = GeneralResultCollector()
        grc.set_container(container)
        ts.set_res_collector(grc)
        ts.search(reg)
        return grc._res
    def proximitySearch(around, word, filepath):
        content = File.getFileContent(filepath)
        ps = ProximitySearch()
        ps.set_proximity_word(around)
        grc = GeneralResultCollector()
        grc.set_container(content)
        ps.set_res_collector(grc)
#         ps.search(NameDicExp("id=\"", "value", ".*","\"").get())
        ps.search(word)
#         ps._collector._data[a:b].replace("id=","").strip('"').replace("message", "")
        return ps._collector.get_results()[0]
class IResultCollector:
    def add_to_results(self, val):
        pass
    def get_results(self):
        pass
    def get_container(self):
        pass
    def reset_result_container(self):
        pass
class ISearch:
    def search(self, word, case=False, reg=False):
        pass
    def set_res_collector(self, collector: IResultCollector):
        pass
class GeneralResultCollector(IResultCollector):
    def __init__(self, empty_container=None):
        if empty_container is None:
            empty_container = []
        self._res = empty_container
        self.set_adder_func(lambda st, val: st._res.append(val))
        self.set_resetable_func(lambda st: st._res.clear())
    def set_container(self, container):
        self._data = container
    def add_to_results(self, val):
        self._func(self, val)
    def set_adder_func(self, func):
        self._func = func
    def get_results(self):
        return self._res
    def get_container(self):
        return self._data
    def set_resetable_func(self, func):
        self._reset_func = func
    def reset_result_container(self):
        self._reset_func(self)
class TextListSearch(ISearch):
    def __init__(self):
        self.set_break_after_first_found()
    def set_break_after_first_found(self):
        self._break = True
    def search(self, word, case=False, reg=False):
        lines = self._collector.get_container()
        from useful.ComparerDB import ComparerDB
        for i, line in lines:
            if ComparerDB.has(word, line, case, reg):
                self._collector.add_to_results(i)
                if self._break:
                    break
    def set_res_collector(self, collector: IResultCollector):
        self._collector = collector
class TextSearch(ISearch):
    def search(self, regex):
        from WordDB import WordDB
        for found in WordDB.searchWordWithRegex(regex, self._collector.get_container()):
            self._collector.add_to_results(found)
    def set_res_collector(self, collector: IResultCollector):
        self._collector = collector
class ProximitySearch(TextSearch):
    def __init__(self):
        self._near_pos = None
        self.set_index_for_proximity_word(0)
    def set_proximity_word(self, regex):
        self._word = regex
    def _get_near_pos(self):
        self._res = Main.textSearch(self._word, self._collector.get_container())
        if len(self._res) == 0:
            raise IOError("no words are found")
        if len(self._res) > 1:
            print(f"Many words founds. Selecting word with index {self._pos}")
        self._near_pos = self._res[self._pos]
    def set_index_for_proximity_word(self, index):
        self._pos = index
    def search(self, regex):
        if self._near_pos is None:
            self._get_near_pos()
        l, r = self._near_pos
        content = self._collector.get_container()
        left_content = content[:l]
        right_content = content[r:]
        left_founds = Main.textSearch(regex, left_content)
        right_founds = Main.textSearch(regex, right_content)
        self._add_logic(left_founds, right_founds, l, r)
    def _add_logic(self, left_founds, right_founds, l, r):
        from MathObjectDB import Range
        if len(left_founds) != 0:
            a = left_founds[-1]
            if len(right_founds) != 0:
                b = right_founds[0]
                if Range(*a).calcDistance(Range(l,r)) < Range(*b).calcDistance(Range(l,r)):
                    self._collector.add_to_results(a)
                else:
                    self._collector.add_to_results(b)
            else:
                self._collector.add_to_results(a)
        else:
            if len(right_founds) != 0:
                b = right_founds[0]
                self._collector.add_to_results(b)
class TelegramHtmlSearch(ISearch):
    def __init__(self):
        self.set_res_collector(GeneralResultCollector({}))
        self._is_parsed = False
    def set_res_collector(self, collector: IResultCollector):
        self._collector = collector
    def set_htmls(self, html_files):
        self._files = html_files
    def search(self, word, case = False, reg = False):
        from SearchSystem import DicSearch
        from modules.SearchSystem.modular import GDisplayableResult, JupyterResultDisplayer, DisplayNElement
        from FileDatabase import ChromeHtmlFileOpenerWithHashTag
        if not self._is_parsed:
            self._load_files()
        cr = ChromeHtmlFileOpenerWithHashTag()
        content = self._collector.get_container()
        val = []
        for path in content:
            dic = content[path]
            ds = DicSearch(dic)
            message_path = lambda n: path + f"#go_to_message{n.replace('message','')}"
            val += [GDisplayableResult(n.replace("message",""), message_path(n),message_path(n) )
                                        for n in ds.search(word, case, reg)]
        jrd = JupyterResultDisplayer()
        jrd.set_callback(cr.openIt)
        de = DisplayNElement()
        de.set_limit(30)
        jrd.set_result(val)
        jrd.set_displayer_way(de)
        jrd.display()
        
        
    def _load_files(self):
        from FileDatabase import File
        from htmlDB import htmlDB
        self._collector.set_container({})
        for file in self._files:
            soup = htmlDB.getParsedData(File.getFileContent(file))
            messages = soup.find_all(attrs={'class': ['message']})
            user_messages = list(filter(lambda x: 'message-' not in x['id'], messages))
            dic = {}
            for val in user_messages:
                dic[val['id']] = ("".join(list(val.strings))).strip()
            self._collector.get_container()[file] = dic
        self._is_parsed = True
class TelegramChannels:
    def __init__(self, display_sub_channel = False):
        self.db = None
        self._tpath = r"D:\TimeLine\2022\telegram-channels"
        self._disp = display_sub_channel
    def search(self, word, case=False, reg=False):
        import os
        from modules.SearchSystem.modular import JupyterResultDisplayer, GDisplayableResult, DisplayNElement
        from SearchSystem import DicSearch
        cpaths = os.listdir(self._tpath)
        dic = {a:a for a in cpaths}
        ds = DicSearch(dic)
        jrd = JupyterResultDisplayer()
        jrd.set_displayer_way(DisplayNElement())
        jrd.set_result([GDisplayableResult(n, '', n) for n in ds.search(word,case,reg)])
        jrd.set_callback(self._callback)
        jrd.display()
    def get(self):
        return self.db
    def _callback(self, val):
        from Path import Path
        from nice_design.search import TelegramHtmlSearch
        from modules.Explorer.personalizedWidgets import Main
        htmls = Path.filesWithExtension("html", Path.joinPath(self._tpath, val))
        ths = TelegramHtmlSearch()
        ths.set_htmls(htmls)
        self.db = ths
        if self._disp:
            display(Main.gui_for_db(self.db))