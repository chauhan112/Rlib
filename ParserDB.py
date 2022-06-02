from ListDB import ListDB
import yaml
class ParserDB:
    def parseBlock(contentInfos):
        txt = ''
        lastLvl = None
        for value,lineNr, lvl in sorted(contentInfos, key=lambda arr: arr[1]):
            if(lastLvl is not None):
                if(lvl > lastLvl):
                    txt += ":"
                txt += "\n"
            txt +=  "  "*lvl + "- " +value.replace("'","\'")# + "'"
            lastLvl = lvl
        return yaml.safe_load(txt)
    
    def parsePythonLikeSyntax(content):
        content = content.strip().split("\n")
        g = []
        for i, line in enumerate(content):
            # if(lien)
            founds = WordDB.searchWordWithRegex("^[ ]+", line)
            lvl = 0
            if(len(founds) != 0):
                lvl = WordDB.searchWordWithRegex("^[ ]+", line)[0][-1]

            g.append((line, i, lvl))
        return ParserDB.parseBlock(g)
    
    def parseNumerikLikeContent(contentList):
        from ExampleDB import ExampleDB
        return ExampleDB.parsingNumerikContent(contentList)

    def getFunctions(content):
        from FileDatabase import File
        from CodeDB import CodeDB
        from Path import Path
        filePath = "temp.py"
        File.overWrite(filePath, content)
        p = CodeDB.parseFile(filePath)
        Path.delete([filePath])
        funcs = [f"def {f}:\n{p.getFunctionContent(f)}" for f in p.functions()]
        return funcs

    def blockParser(arr, determiner, valFunc = lambda x: x):
        import collections
        de = collections.deque(arr)
        l = collections.deque([])
        groups = []
        while (len(de) != 0):
            k = de.popleft()
            if(determiner(k[0])):
                l.append(k)
            else:
                groups.append((valFunc(l.pop()), valFunc(k)))
        if(len(l) != 0):
            print(l)
            raise IOError("Wrong format")
        return groups