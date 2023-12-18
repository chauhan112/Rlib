from ListDB import ListDB
import yaml
from WordDB import WordDB
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
    def mergeDic(dicList):
        newDic = {}
        for chapter in dicList:
            newDic.update(chapter)
        return newDic
    def parseNumerikLikeContent(content):
        numerikContent = yaml.safe_load(File.getFileContent(resourcePath() +"examplesDB.yaml"))['numerik'].split("\n")
        if(content is not None):
            numerikContent = content
        content = list(filter(lambda l: WordDB.searchWordWithRegex("^[0-9]+" , l.strip()), numerikContent))
        content = [(val, i) for i, val in enumerate(content)]

        mapFunction = lambda l: len(WordDB.searchWordWithRegex("[0-9]+\.", l[0]))

        g= OpsDB.grouper(mapFunction, content)
        newG = []
        for key in g:
            for val,i in g[key]:
                newG.append(("".join([val[i-1:j] for i, j in WordDB.searchWordWithRegex("[a-zA-Z]+", val)]).strip(),
                i, key))
        return ParserDB.mergeDic(ParserDB.parseBlock(newG))
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
        
from RegexDB import RegexDB
class CustomParser:
    def parser_layers(content):
        pass
class TypeScriptParser:
    def parse_layers2(content):
        layer = 0
        blocks = [0]
        mmp = {}
        tt = ""
        lineNr = 0
        for i, l in enumerate(content):
            if l == "{":
                TypeScriptParser._add(mmp, (layer, blocks[layer]), (lineNr, tt))
                tt = ""
                blocks[layer] += 1
                layer += 1
                blocks.append(0)
            elif l =="}":
                TypeScriptParser._add(mmp, (layer, blocks[layer]), (lineNr, tt))
                tt = ""
                layer -= 1
                blocks.pop()
            elif l == "\n":
                lineNr += 1
            else:
                tt += l
        return mmp
    def parse_layers3(content):
        layer = 0
        mmp = {}
        tt = ""
        lineNr = 0
        skip = False
        for i, l in enumerate(content):
            if l == "{":
                TypeScriptParser._add(mmp, layer, (lineNr, tt))
                tt = ""
                skip = True
                layer += 1
            elif l =="}":
                skip = True
                TypeScriptParser._add(mmp, layer, (lineNr, tt))
                tt = ""
                layer -= 1
            elif l == "\n":
                lineNr += 1
                if not skip:
                    TypeScriptParser._add(mmp, layer, (lineNr, tt))
                tt = ""
            else:
                skip = False
                tt += l
        return mmp
    def _add(mmp, key, value):
        if key not in mmp:
            mmp[key] =[]
        mmp[key].append(value)
    def remove_comments(content):
        pass
    def remove_single_line_comments(content:str):
        lines = content.splitlines()
        return "\n".join(map(lambda line: RegexDB.replace("//.*", line, lambda x: ""), lines))
    def remove_empty_lines(content):
        lines = content.splitlines()
        return "\n".join(filter(lambda line: len(line.strip()) != 0, lines))