from ancient.CodeDB import CodeDB
class TracebackDB:
    def getFunctionName(lineNr, filepath):
        pass

    def findFunctionCall(file, lineNr):
        p = CodeDB.parseFile(file)
        functionsRange = {}
        for func in p.functions():
            functionsRange[func] = p.getFunctionRange(func)
            
        for func in functionsRange:
            r = functionsRange[func]
            if(lineNr >= r[0]  and lineNr <= r[1]):
                return func
        return ("No function Found")