from ParserDB import ParserDB
from WordDB import WordDB
from OpsDB import OpsDB
import yaml
from FileDatabase import File
from LibPath import *

class ExampleDB:
    def parsingNumerikContent(content = None):
        numerikContent = yaml.safe_load(File.getFileContent(getPath() +"\\resource\\examplesDB.yaml"))['numerik'].split("\n")
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
        return ExampleDB.mergeDic(ParserDB.parseBlock(newG))

    def parsingPhilosophyContent():
        content = yaml.safe_load(File.getFileContent(getPath() +"\\resource\\examplesDB.yaml"))['philosophy'].strip().split("\n")
        content = list(filter(lambda l: WordDB.searchWordWithRegex("^[0-9]+" , l.strip()), content))

        exp1 = "^.*?(?=[a-zA-Z])"
        exp2 = "(?<= )[a-zA-Z\-,’]+"

        k = []
        for index,cont in enumerate(content):
            k.append((" ".join([cont[i:j] for i, j in WordDB.searchWordWithRegex(exp2, cont)]), index,
                    len([cont[i:j] for i, j in WordDB.searchWordWithRegex(exp1, cont)][-1].split("."))))
        return ExampleDB.mergeDic(ParserDB.parseBlock(k))
    def mergeDic(dicList):
        newDic = {}
        for chapter in dicList:
            newDic.update(chapter)
        return newDic

    def invalidCode_startUnzipProcess(homeworkPath, zipFile):
        zipFile = homeworkPath + os.sep + os.path.basename(zipFile)
        if("zip" not in zipFile):
            zipFile = zipFile + ".zip"
            
        pathsInZip = ZipTools.getMyStudentFilePaths( zipFile )
        tocheck = homeworkPath + os.sep + "to check"
        ZipTools.unzipFilesFromZipWithPaths(zipFile, pathsInZip, tocheck)
        print(str(len(pathsInZip)) + " files extracted to " + tocheck )
        zipPaths = Path.filesWithExtension("zip", tocheck)
        Path.move().files(zipPaths, tocheck)
        print(str(len(zipPaths)) + " zip files moved to "+ tocheck)
        zipPaths = Path.filesWithExtension("zip", tocheck)
        ZipTools.extractAllZipsToPath(zipPaths, tocheck)
        Path.delete(zipPaths)
    
    def renamingPdfFiles(path):
        komsys = r"D:\cloud\timeline\fourth semester\Komsystem\data\scripts"
        pdfs = Path.filesWithExtension("pdf", komsys)
        """pdfs
        ['D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationsssysteme_5_Einfuehrung_IP_Adressen_small.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationsssysteme_6_CIDR.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationsssystem_14_UDP.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_08_NAT.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_09_Routingprotokolle.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_10_ARP_ICMP_IP.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_11_SendWait.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_12_SlidingWindow.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_13_TCP.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_16_DNS.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_17_Anwendungsprotokolle.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_18_Einfuehrung_Sicherungsschicht_Netztechnik.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_1_Einfuehrung_small.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_2_Schichtenmodell_small.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_3_Sockets.pdf',
         'D:\\cloud\\timeline\\fourth semester\\Komsystem\\data\\scripts\\Kommunikationssysteme_4_Darstellung_small.pdf']
        """
        def rename(filepath):
            path = os.path.dirname(filepath)
            name = os.path.basename(filepath)
            nr = [name[i:j] for i,j in WordDB.searchWordWithRegex("[0-9]+", name)][0]
            if(len(nr) == 1):
                nr = '0'+ nr
            name = nr + "_" + [name[i:j] for i,j in WordDB.searchWordWithRegex("(?<=[0-9]_).*", name)][0]
            return Path.joinPath(path, name)
        Path.renameAllFiles(pdfs, rename)