from useful.basic import Main as ObjMaker
from FileDatabase import File

def LanguageParser():
    content = ""
    langComps = {"[": "]", "{":"}", "(":")", "'":"'", '"':'"'}
    langCompsReversed = {langComps[k]: k for k in langComps}
    def set_lang_components(comps):
        s.process.langComps = comps
        s.process.langCompsReversed =  {comps[k]: k for k in comps}
    def parse_linear_res():
        res = []
        counterQueue = {}
        for i, c in enumerate(s.process.content):
            if c in s.process.langComps:
                if c not in counterQueue:
                    counterQueue[c] = []
            if c in s.process.langComps and c in s.process.langCompsReversed:
                if len(counterQueue[langCompsReversed[c]]):
                    grou = counterQueue[langCompsReversed[c]].pop()
                    grou.append(i)
                    res.append(grou)
                else:
                    counterQueue[c].append([i])
            elif c in s.process.langComps:
                counterQueue[c].append([i])
            elif c in s.process.langCompsReversed:
                if len(counterQueue[langCompsReversed[c]]):
                    grou = counterQueue[langCompsReversed[c]].pop()
                    grou.append(i)
                    res.append(grou)
        return res
    def get_node(start=0, end=-1):
        node = ObjMaker.namespace()
        node.start = start
        node.end = end
        node.value = s.process.content[start]
        node.children = []
        return node
    def pop(queue):
        if len(queue) > 1:
            queue.pop()
    def parse_with_parent_child():
        root = s.handlers.get_node()
        queue = [root]
        for i in range(len(s.process.content)):
            c = s.process.content[i]
            if c in s.process.langComps or c in s.process.langCompsReversed:
                current = queue[-1]
                if c in s.process.langComps and c in s.process.langCompsReversed:
                    if current.value == c:
                        current.end = i
                        s.handlers.pop(queue)
                    else:
                        node = s.handlers.get_node(i)
                        current.children.append(node)
                        queue.append(node)
                elif c in s.process.langComps:
                    node = s.handlers.get_node(i)
                    current.children.append(node)
                    queue.append(node)
                elif c in s.process.langCompsReversed:
                    current.end = i
                    s.handlers.pop(queue)
        return root
    def bfs(root, condition, allRes = False):
        queue = [root]
        res = []
        while True:
            node = queue.pop()
            if condition(node):
                if allRes:
                    res.append(node)
                else:
                    return node
            for ch in node.children:
                queue.append(ch)
            if len(queue) == 0:
                break
        return res
    s = ObjMaker.variablesAndFunction(locals())
    return s
def StringManipulation():
    content = ""
    fromIndex = 0
    lastIndex = -1
    results = None
    def findFirstIndex(finderList, reg= False):
        pass
    def findLastIndex(finderList, reg=False):
        pass
    def narrowTheDomain():
        pass
    def iterator(condition, allRes=False, container=None):
        if container is None:
            container = s.process.content
        res = []
        for i, c in enumerate(container):
            if condition(i, c):
                if not allRes:
                    return i
                res.append(i)
        return res
    def replaceWith(newText, including=True):
        return s.process.content[:s.process.fromIndex] + newText + s.process.content[s.process.lastIndex + int(including): ]
    def matchBefore(index, contentToMatch, allContent):
        newIndex = index - len(contentToMatch)
        if newIndex >= 0:
            return allContent[newIndex: index] == contentToMatch
        return False
    s = ObjMaker.variablesAndFunction(locals())
    return s
def TailWindSafeListReplacer():
    # filePath = r".\react-projects\tailwind.config.js"
    filePath = None
    content = ""
    strManip = StringManipulation()
    langParser = LanguageParser()
    
    root = None
    def condition(node):
        if node.value == "{":
            if s.process.strManip.handlers.matchBefore(node.start, "module.exports = ", s.process.strManip.process.content):
                return True
        return False
    def replace(newContent):
        if s.process.filePath is None:
            raise IOError("please set a file path")
        s.process.content = File.getFileContent(s.process.filePath)
        s.process.strManip.process.content = s.process.content
        s.process.langParser.process.content = s.process.content
        s.process.root = s.process.langParser.handlers.parse_with_parent_child()
        res_node = s.process.langParser.handlers.bfs(s.process.root, s.handlers.condition)
        res_node = s.process.langParser.handlers.bfs(res_node, lambda node: s.process.strManip.handlers.matchBefore(node.start, "safelist: ", s.process.content))
        s.process.strManip.process.fromIndex = res_node.start
        s.process.strManip.process.lastIndex = res_node.end
        return s.process.strManip.handlers.replaceWith(newContent)
    def write_to_file():
        File.overWrite(s.process.filePath, s.process.strManip.handlers.replaceWith(newContent))
    s = ObjMaker.variablesAndFunction(locals())
    return s
def LanguageParserV2():
    """Multi syntax parser. Can handle all types"""
    content = ""
    langComps = {"[": "]", "{":"}", "(":")", "'":"'", '"':'"'}
    langCompsReversed = {langComps[k]: k for k in langComps}
    i = 0
    windowSize = 1
    def set_lang_components(comps):
        s.process.langComps = comps
        s.process.langCompsReversed =  {comps[k]: k for k in comps}
        s.process.sizes = set(map(len, comps)).union(set(map(len, s.process.langCompsReversed)))
    def get_node(typ=""):
        node = ObjMaker.namespace()
        node.start = s.process.i
        node.end = node.start + s.process.windowSize
        node.value = s.process.content[node.start: node.end]
        node.typ = typ
        node.children = []
        return node
    def pop(queue):
        if len(queue) > 1:
            queue.pop()
    def parse_with_parent_child():
        root = s.handlers.get_node()
        queue = [root]
        s.process.i = 0
        s.process.windowSize = 1
        
        while s.process.i < len(s.process.content):
            a,b = s.handlers.existsInLang()
            if a or b:
                current = queue[-1]
                if a and b:
                    if current.value == s.process.c:
                        current.end = s.process.i + s.process.windowSize
                        s.handlers.pop(queue)
                    else:
                        node = s.handlers.get_node(s.process.c)
                        current.children.append(node)
                        queue.append(node)
                elif a:
                    node = s.handlers.get_node(s.process.c)
                    current.children.append(node)
                    queue.append(node)
                elif b:
                    if s.process.langCompsReversed[s.process.c] == current.typ:
                        current.end = s.process.i + s.process.windowSize
                        s.handlers.pop(queue)
            s.process.i += s.process.windowSize
        return root
    def existsInLang():
        for ws in s.process.sizes:
            s.process.windowSize = ws
            s.process.c = s.process.content[s.process.i: s.process.i + ws]
            if s.process.c in s.process.langComps:
                return True, s.process.c in s.process.langCompsReversed
            if s.process.c in s.process.langCompsReversed:
                return False, True
        s.process.windowSize = 1
        return False, False
    def _exists():
        s.process.c = s.process.content[s.process.i]
        return s.process.c in s.process.langCompsReversed
    def bfs(root, condition, allRes = False):
        queue = [root]
        res = []
        while True:
            node = queue.pop()
            if condition(node):
                if allRes:
                    res.append(node)
                else:
                    return node
            for ch in node.children:
                queue.append(ch)
            if len(queue) == 0:
                break
        return res
    s = ObjMaker.variablesAndFunction(locals())
    return s

class Main:
    def example():
        tws = TailWindSafeListReplacer()
        tws.process.filePath =  r".\react-projects\tailwind.config.js"
        print(tws.handlers.replace("[adwd]"))
    def cssContentParser():
        # returns list of key and value where key is the class name and value is the content inside 
        # curly bracket
        content = """.jc-sb{
                justify-content: space-between;
            }
            .jc-sp{
                justify-content: space-between;
            }
            .p0{
                margin: 0;
                padding: 0
            }
            .w-100{
                width: 100%
            }
            .flex{
                display: flex;
            }
            .flex-column{
                flex-direction: column
            }
            .flex-1{
                flex: 1
            }
            .w-50{
                width: 50%
            }
            .w-90{
                width: 90%
            }
            .w-auto{
                width: auto
            }
            .color-white{
                color: white
            }
            .bg-color-unset{
                background-color: unset
            }
            .bg-blue-light{
                background-color: #007bff
            }
            .hmin-200px textarea{
               min-height: 200px;
            } 
            .hmin-300px textarea{
                min-height: 300px;
            }
            .pointerNone{
                pointer-events: none
            }
            .pointerAll{
            pointer-events: all

            }
            .block{
               display: block;
            }
            .w-fit{
               width: fit-content;
            }
            .br-5px{
               border-radius: 5px
            }
            .h-100{
               height: 100%
            }
            .grid{
               display: grid;
            }
            .grid-responsive{
                grid-template-columns: repeat(auto-fit, minmax(min(100px, 100%), 1fr));
            }
            .h-150px{
                height: 150px;
            }
            .order-1{
                order: 1
            }
            .grid-column-repeat-auto-7{
                grid-template-columns: repeat(6,auto);
            }
            .span-all-columns{
                grid-column: 1/-1;
            }
            .textarea-h-150px textarea{
                height: 150px;
            }
            .flex-wrap{
                flex-wrap: wrap;
            }
            .w-150px{
               width: 150px;
            }
            .overflow-hidden{
                overflow: hidden;
            }
            .overflow-unset{
                overflow: unset;
            }
            .overflow-visible{
                overflow: visible;
            }
            .mw-100px{
                max-width: 100px;
            }
        """
        from timeline.t2024.Array import Array
        def get_class_name(node):
            res = ""
            index = node.start-1
            while True:
                if index < 0:
                    return res
                c = langParser.process.content[index]
                if c == "}":
                    return res
                else:
                    res = c + res
                index -= 1
        langParser = LanguageParser()
        langParser.handlers.set_lang_components({'{':'}'})
        langParser.process.content = content
        root = langParser.handlers.parse_with_parent_child()
        results = Array(root.children).map(lambda x: (get_class_name(x).strip(), langParser.process.content[x.start + 1: x.end].strip())).array
        results