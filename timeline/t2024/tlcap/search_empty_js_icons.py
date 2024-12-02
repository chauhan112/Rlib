from timeline.t2024.tailwind.tailwind_config_modify import LanguageParserV2
from timeline.t2024.Array import Array
def isEmpty(content):
    removedComment = RemoveJSComments(content)
    return len(removedComment) == 0
def RemoveJSComments(content):
    langParser = LanguageParserV2()
    langParser.handlers.set_lang_components({'/*':'*/', "//": "\n"})
    langParser.process.content = content
    root = langParser.handlers.parse_with_parent_child()
    results = Array(root.children).map(lambda x: langParser.process.content[x.start: x.end].strip()).array
    newContent = ""
    l = 0
    for x in root.children:
        newContent += langParser.process.content[l: x.start]
        l = x.end
    newContent += langParser.process.content[l:]
    return newContent.strip()
def flowsChecker(flows):
    for f in flows:
        founds = jsElementDetector(f['icon'])
        # print(f["name"])
        if len(founds) > 0:
            print("---"+ f["name"] + "---")
def flowsGetter(moduleName="", dic=None):
    if "flows" in dic["resources"]:
        # print(moduleName)
        print("--"* 20)
        flowsChecker(dic["resources"]["flows"])
        print("--"* 20)
    if "resolvedIncludes" in dic:
        for ri in dic["resolvedIncludes"]:
            flowsGetter(ri["pk"], ri)
def hasConsole(content):
    removedComment = RemoveJSComments(content)
    return "console.log" in removedComment
def findAllLocsWithConsoleLogInJsIcon(filePath):
    loadedJSON = json.loads(File.getFileContent(filePath))
    dm = DictionaryModel()
    dm.s.process.model = loadedJSON
    sid = SearchInDictionary()
    sid.set_search_func(lambda x,y: x==y)
    sid.set_dic(loadedJSON)
    founds = sid.search("JAVASCRIPT")
    nf = NameFinder()
    nf.set_data(loadedJSON)
    
    res = []
    for i, f in enumerate(founds):
        content = dm.read(f[0][:-1] +["input", "code"])
        if hasConsole(content):
            nf.set_location(LocationData(f[0]))
            res.append((f[0],nf.get_name()))
    return res
    
   
# flowsGetter("main app", dm.read(["result"]))