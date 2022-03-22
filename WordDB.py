import re
import yaml
from FileDatabase import File
import difflib

class WordDB:
    def isWord(string, escapeChar = ['_']):
        for char in string:
            if( not ((char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or char in escapeChar )):
                return False
        return True

    def getNextWord(pos, content, escapeChar=['-', '_']):
        word = ""
        for i in range(pos, len(content)):
            char = content[i]
            if( (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or char in escapeChar ):
                word += char
            else:
                break
        return word

    def getRemainingContent(word, content):
        i = 0
        foundAt = WordDB.searchWordWithRegex(word, content)
        remainingText = ""
        for start, end in foundAt:
            remainingText += content[i:start]
            i = end
        return remainingText

    def searchWordWithRegex(regex,content):
        matches = re.finditer(regex, content)
        found = []
        for i,match in enumerate(matches):
            found.append([match.start(),  match.end()])
        return found

    def getSpecialWords():
        specialWord = {
            "words": [],
            "urlRegEx" : "",
            "emailRegEx": "",
        }
        return specialWord
        
    def getWordFrequencyCount(arr, sort = True):
        freq = {}
        for val in arr:
            try:
                freq[val] += 1
            except:
                freq[val] = 1
        if(sort):
            return {k: v for k, v in sorted(freq.items(), key=lambda item: item[1])}
        return freq
    
    def regexMatchFound(regex, line):
        k = re.search(regex,line)
        return k != None
    
    def regexExamples():
        from IPython.display import HTML
        k = """
        <p>Given the string <code>foobarbarfoo</code>:</p>
        <pre class="default prettyprint prettyprinted" style=""><code><span class="pln">bar</span><span class="pun">(?=</span><span class="pln">bar</span><span class="pun">)</span><span class="pln">     finds the </span><span class="lit">1st</span><span class="pln"> bar </span><span class="pun">(</span><span class="str">"bar"</span><span class="pln"> which has </span><span class="str">"bar"</span><span class="pln"> after it</span><span class="pun">)</span><span class="pln">
        bar</span><span class="pun">(?!</span><span class="pln">bar</span><span class="pun">)</span><span class="pln">     finds the </span><span class="lit">2nd</span><span class="pln"> bar </span><span class="pun">(</span><span class="str">"bar"</span><span class="pln"> which does </span><span class="kwd">not</span><span class="pln"> have </span><span class="str">"bar"</span><span class="pln"> after it</span><span class="pun">)</span><span class="pln">
        </span><span class="pun">(?&lt;=</span><span class="pln">foo</span><span class="pun">)</span><span class="pln">bar    finds the </span><span class="lit">1st</span><span class="pln"> bar </span><span class="pun">(</span><span class="str">"bar"</span><span class="pln"> which has </span><span class="str">"foo"</span><span class="pln"> before it</span><span class="pun">)</span><span class="pln">
        </span><span class="pun">(?&lt;!</span><span class="pln">foo</span><span class="pun">)</span><span class="pln">bar    finds the </span><span class="lit">2nd</span><span class="pln"> bar </span><span class="pun">(</span><span class="str">"bar"</span><span class="pln"> which does </span><span class="kwd">not</span><span class="pln"> have </span><span class="str">"foo"</span><span class="pln"> before it</span><span class="pun">)</span></code></pre>
        """
        return HTML(k)

    def replaceWithRegex(regex,replacingPart,  text):
        return re.sub(regex, replacingPart, text)

    def getLineRanges(content):
        lineRanges = []
        i = 0
        for line in content.split("\n"):
            lineRanges.append([i, i +len(line)])
            i += len(line)
        return lineRanges
    
    def intWordFormat(nr, spaceNr):
        k = spaceNr - len(str(nr))
        if(k <1):
            return str(nr)
        return " "*k + str(nr)
    
    def replaceOneAfterAnother(mainString, replacing):
        for rStr, replaceWith in replacing:
            mainString = mainString.replace(rStr, replaceWith)
        return mainString
    
    def regexSplit(regex, string):
        return re.split(regex, string)

    def getLink(value):
        from WordDB import WordDB
        regex = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
        if(ComparerDB.regexSearch(regex, value)):
            i,j = WordDB.searchWordWithRegex(regex, value)[0]
            filteredValue = value[i:j]
            return filteredValue.split('"')[0]

    def stringDiffMultiline(first,second):
        for text in difflib.unified_diff(first.split("\n"), second.split("\n")):
            if text[:3] not in ('+++', '---', '@@ '):
                print (text)

    def formatSyntax(word = None):
        from Database import Database
        from SerializationDB import SerializationDB
        from LibsDB import LibsDB
        
        val = SerializationDB.readPickle(LibsDB.picklePath("GeneralDB.pkl"))['string format']
        db = Database.getDB( [str(i)  for i in list(range(len(val)))], val, 
                            displayer=lambda x: print(val[int(x)]),
                        keysFilter= lambda x: val[int(x)][3])
        
        if(word is not None):
            db.search(word)
        return db
        
    def stringDiff(a, b, verbose = False):
        for i,s in enumerate(difflib.ndiff(a, b)):
            if(verbose):
                if s[0]==' ': continue
                elif s[0]=='-':
                    print(u'Delete "{}" from position {} of first string'.format(s[-1],i))
                elif s[0]=='+':
                    print(u'Add "{}" at position {} to first string'.format(s[-1],i))   
            else:
                print(s)

    def replace():
        class WordReplace:
            def replace(word, replaceWith, text):
                return text.replace(word, replaceWith)

            def withRegex(regex, replaceWith, text):
                return re.sub(regex, replaceWith, text)

            def withFunc(regex, replacingFunc, text):
                i = 0
                foundAt = WordDB.searchWordWithRegex(regex, text)
                newText = ""
                for start, end in foundAt:
                    word = text[start:end]
                    newText += text[i:start] + replacingFunc((start, end, word))
                    i = end
                newText += text[i:]
                return newText

            def withContainers(regOrWord, wordContainer, text):
                # number of outputs are already known 
                # word container contains same number of word or it be use cycled
                i = 0
                foundAt = WordDB.searchWordWithRegex(regOrWord, text)
                n = len(wordContainer)
                newText = ""
                for j, (start, end) in enumerate(foundAt):
                    word = text[start:end]
                    newText += text[i:start] + wordContainer[j%n]
                    i = end
                newText += text[i:]
                return newText

            def oneAfterAnother(mainString, replacingTuple):
                for rStr, replaceWith in replacingTuple:
                    mainString = mainString.replace(rStr, replaceWith)
                return mainString
        return WordReplace
        
    def formatting():
        class Temp:
            def integer(number, nSpace, space=""):
                f = "{:"+ str(space) + ">" + str(nSpace) + "d}"
                return f.format(number)
            def floatVal(number, afterDecimal= 2):
                tt = f"{{:.{afterDecimal}f}}"
                return tt.format(number)
            def word(word, nLetter=10, align = "<"):
                skele = '{word:'+align+str(nLetter)+'s}'
                return skele.format(word=word)
            
        return Temp
    
    def tokenize(content):
        return list(set([content[i:j] for i, j in WordDB.searchWordWithRegex('\w+',content)]))
        
    def commonPart(stringList):
        # inp = ['abc', 'abd']
        # out = 'ab'
        assert len(stringList) > 0
        def common(s1, s2):
            co = ''
            for i, ch in enumerate(s1):
                try:
                    if(s2[i] == ch):
                        co += ch
                except:
                    break
            return co
        
        com = stringList[0]
        for s2 in stringList[1:]:
            com = common(com, s2)
        return com