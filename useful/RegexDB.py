from useful.WordDB import WordDB
import os
from useful.LibsDB import LibsDB
from useful.SerializationDB import SerializationDB
from useful.Database import Database
class NameDicExp:
    def __init__(self, beforename, name:str,name_reg:str, aftername):
        temp = [beforename, name,name_reg, aftername]
        self.data = []
        for vla in temp:
            if isinstance(vla, NameDicExp):
                self.data.append(vla.get())
            else:
                self.data.append(vla)
    def get(self):
        beforename, name,name_reg, aftername = self.data
        return beforename + f"(?P<{name}>{name_reg})" + aftername
class RegexDB:
    def lookAhead(aheadString, regex):
        return f"(?<={aheadString}){regex}"
    def lookBehind(behindStr, regex):
        return f"{regex}(?={behindStr})"
    def regexSearch(regex,content):
        return [content[i:j] for i, j in WordDB.searchWordWithRegex(regex,content)]
    def lookAheadAndBehind(ahead, behind, regex):
        return f"(?<={ahead}){regex}(?={behind})"
    def isThereRegexMatch(regex, content):
        return WordDB.regexMatchFound(regex, content)
    def replace(regex,text, replacingFunc):
        founds = WordDB.searchWordWithRegex(regex, text)
        newText = ''
        l = 0
        for a,b in founds:
            newText += text[l:a]
            newText += replacingFunc(text[a:b])
            l = b
        newText += text[l:]
        return newText
    def group_name_search(exp:NameDicExp, text):
        """
        * only works for a single line because you are defining the entire structure
        """
        if type(exp) == str:
            reg = exp
        else:
            reg = exp.get()
        import re
        reg = re.compile(reg)
        f = reg.match(text)
        if f is not None:
            return f.groupdict()
        return {}