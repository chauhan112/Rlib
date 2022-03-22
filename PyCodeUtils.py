class PyCodeUtils:
    def encodedParser(content):
        import yaml
        from RegexDB import RegexDB
        
        def spaceCount(line):
            val = RegexDB.regexSearch("^( |\t)+",line)
            if(val == []):
                return 0
            return len(val[0])
        
        exampleFileContent = PyCodeUtils.pyCommentRemover(content)
        lines = exampleFileContent.splitlines()
        yamlText = "" # layer1
        first = False
        inside = True
        lastCo = None
        for i,line in enumerate(lines):
            if(len(line.strip()) == 0):
                yamlText += "\n"
                continue
            co = spaceCount(line)

            if( line.strip()[-1] == ':'):
                yamlText += " "*co + f'{i}:\n'
                inside = True
            else:
                yamlText += " "*co + f'{i}: {i}\n'
                
        layer2 = ""
        lastline = None
        for line in yamlText.splitlines():
            sp = spaceCount(line)
            if(lastline is not None):
                if(sp > spaceCount(lastline)):
                    if(not lastline.endswith(":")):
                        sp = spaceCount(lastline)
            lastline = " "*sp + line.strip()
            layer2 += lastline+"\n"
            
        return yaml.safe_load(layer2)

    def pyCommentRemover(source):
        import io, tokenize, re
        io_obj = io.StringIO(source)
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            ltext = tok[4]
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
            if token_type == tokenize.COMMENT:
                pass
            elif token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
                    if prev_toktype != tokenize.NEWLINE:
                        if start_col > 0:
                            out += token_string
            else:
                out += token_string
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line
        out = '\n'.join(l for l in out.splitlines() if l.strip())
        return out

    def getFunctionNames(pyFileContent):
        from PyCodeUtils import PyCodeUtils
        from RegexDB import RegexDB
        uncommentedContent = PyCodeUtils.pyCommentRemover(pyFileContent)
        return RegexDB.regexSearch(RegexDB.lookAheadAndBehind("def ", ":", ".*"),uncommentedContent )
    
    def parseValidLines(content):
        import ast
        if(type(content) == str):
            content = content.split("\n")
        p = []
        for line in content:
            try:
                p.append(ast.parse(line))
            except:
                pass
        return p

    def classNfuncFromAstCall(astCall):
        import ast
        cls = ''
        funcs = []
        if(isinstance(astCall.func, ast.Name)):
            funcs = [astCall.func.id]
        elif(isinstance(astCall.func.value, ast.Name)):
            cls, funcs = astCall.func.value.id, [astCall.func.attr]
        elif(isinstance(astCall.func.value, ast.Call)):
            cls, funcs = getClassNFunctionName(astCall.func.value)
            funcs.append(astCall.func.attr)
        return cls, funcs

    def getClassesUsedNFrequency(content):
        import ast
        cls = {}
        k = parseValidLines(content)
        for module in k:
            for node in ast.walk(module):
                if(isinstance(node, ast.Call)):
                    c, f = classNfuncFromAstCall(node)
                    try:
                        cls[c] += 1
                    except:
                        cls[c] = 1
        return cls
    
class HelperFunctions:
    def pyCommentRemover(content):
        val, mapps,lineBr = HelperFunctions.stringEncoder(content)
        hashRemove = HelperFunctions.removePyCommentsWithHash(val.replace(lineBr, "\n"))
        multiLineRemove = HelperFunctions.removeMultiLineText(hashRemove, list(mapps.keys()))
        res = HelperFunctions.decoder(multiLineRemove, mapps)
        return res.replace(lineBr, "\n")

    def replaceContent(groups, noNewLine):
        from CryptsDB import CryptsDB
        replaceId = f"{CryptsDB.generateRandomName()}comment"
        idNr = 1
        newContent = ""
        mapper = {}
        i = 0
        groups = sorted(groups, key=lambda x: x[0][0])
        for a, b in groups:
            newContent += noNewLine[i:a[0]]
            idVal = f"<{replaceId}{idNr}>"
            mapper[idVal] = noNewLine[a[0]:b[1]]
            newContent += idVal
            i = b[1]
            idNr += 1
        newContent += noNewLine[i:]
        return newContent, mapper

    def reshaper(arr):
        if (len (arr) %2 != 0):
            raise IOError("Odd numbers of content")

        p = []
        i = 0
        while i < len(arr):
            p.append([arr[i], arr[i+1]])
            i += 2
        return p

    def stringEncoder(content):
        from WordDB import WordDB
        from CryptsDB import CryptsDB
        lineBr = "<" +CryptsDB.generateRandomName()+">"
        noNewLine = content.replace("\n", lineBr)
        k = WordDB.searchWordWithRegex('"""',noNewLine )
        k += WordDB.searchWordWithRegex("'''", noNewLine)
        groups = HelperFunctions.reshaper(k)
        val , mapper1 = HelperFunctions.replaceContent(groups, noNewLine)

        sk = WordDB.searchWordWithRegex('"',val )
        sk += WordDB.searchWordWithRegex("'", val)
        sgroups = HelperFunctions.reshaper(sk)
        val2 , mapper2 = HelperFunctions.replaceContent(sgroups, val)
        mapper1.update(mapper2)
        return val2,mapper1 , lineBr


    def removeMultiLineText(encodedString, words):
        lines = encodedString.split("\n")
        newLines = []
        for line in lines:
            if(line.strip() not in words):
                newLines.append(line)
        return '\n'.join(newLines)

    def removeEmptylines(content):
        lines = content.split("\n")
        newLines = []
        for line in lines:
            if(len(line.strip()) != 0):
                newLines.append(line)
        return "\n".join(newLines)

    def decoder(string, decoders):
        for key in decoders:
            string = string.replace(key, decoders[key])
        return string

    def removePyCommentsWithHash(content):
        from WordDB import WordDB
        lines = content.split("\n")
        newLines = []
        for line in lines:
            newLines.append(WordDB.replaceWithRegex("#.*", "", line))
        return "\n".join(newLines)

class Tests:
    def test4regex_checking_whether_hash_is_inside_string(func):
        line1 = "sdnkfnd c \"dfnkdsnc # akefjkjadf\""
        line2 = "s'uiu'dnkfnd c dfnkdsnc # akefjkjadf 'hash is not inside'"
        line3 = "sdn\\#sdfivdkfnd c 'dfnkdsnc # akefjkjadf'"
        line4 = "sdnkfnd c \"\"\"dfnkdsnc # akefjkjadf\"\"\""
        line5 = "sdnkfnd c '''dfnkdsnc # akefjkjadf'''"
        assert func(line1) == True
        assert func(line2) == False
        assert func(line3) == True
        assert func(line5) == True
        assert func(line4) == True
    
