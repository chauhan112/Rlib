from timeline.t2024.tailwind.tailwind_config_modify import LanguageParserV2
from timeline.t2024.Array import Array
from useful.basic import Main as ObjMaker
def LanguageOps():
    def removeCommentsJs(content):
        # removes comment from javascript code. keywords: js, javascript, comment
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
    s = ObjMaker.variablesAndFunction(locals())
    return s