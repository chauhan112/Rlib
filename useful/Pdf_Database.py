import os
import PyPDF2
from useful.Path import Path
import yaml
from useful.FileDatabase import File
import pikepdf
from pikepdf import Pdf
from useful.WidgetsDB import WidgetsDB

from enum import Enum
class PDFOPS(Enum):
    ROTATE = 1
    TRANSLATE = 2
    ZOOM = 3


class PdfOps:
    def __init__(self, name):
        self.name = name

    def getPages(self, ranges):
        pdfContainer = Pdf.new()
        with Pdf.open(self.name) as pdf:
            for rnge in ranges:
                if(type(rnge) == tuple):
                    a, b = rnge
                    for i in range(a,b):
                        pdfContainer.pages.append(pdf.pages[i])
                elif(type(rnge) == int):
                    pdfContainer.pages.append(pdf.pages[rnge])
        return pdfContainer

    def applyOpsOnPageNr(pdf, dicOps):
        # dicOps = {rnag:(opEnum, params), p:(opEnum, params)}
        for key in dicOps:
            if(type(key) == tuple):
                a, b = key
                op, params = dicOps[key]
                for i in range(a, b):
                    if(op == PDFOPS.ROTATE):
                        pdf.pages[i].rotate(params)
            elif(type(key) == int):
                op, params = dicOps[key]
                pdf.pages[key].rotate(params)
        return pdf
    
    def read(self):
        return Pdf.open(self.name)


class PDF:
    def getTextFromPDF(pdfName):
        from io import StringIO
        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.pdfpage import PDFPage
        from pdfminer.pdfparser import PDFParser
        print(pdfName)
        output_string = StringIO()
        texts = []
        size = 0
        progressBar = WidgetsDB.progressBar(PDF.getTotalPageNr(pdfName))
        with open(pdfName, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for i, page in enumerate(PDFPage.create_pages(doc)):
                interpreter.process_page(page)
                txt = output_string.getvalue()[size:]
                size += len(txt)
                progressBar.value = i + 1
                texts.append(txt)
        File.createFile(pdfName[:-3] + 'yaml', yaml.dump(texts))
        return texts
    
    def loadPdfFromText(path):
        if(path.lower().endswith(".pdf")):
            path = PDF.pdf2yamlMapper(path)
        if(not os.path.isfile(path)):
            print("cant read file convert to text first")
            raise IOError()
        return yaml.safe_load(File.getFileContent(path))
    
    def getTotalPageNr(pdfName):
        with open(pdfName, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            return reader.getNumPages()
    
    def exportToYaml(bookContentArray,bookName, path = None):
        if(path is None):
            path = os.getcwd()
        File.createFile(path + os.sep + bookName,yaml.dump(bookContentArray))
    
    def unlockPdf(pdfFile, password=''):
        file_path = pdfFile.replace('\\','/')
        init_pdf = pikepdf.open(file_path, password)
        new_pdf = pikepdf.new()
        new_pdf.pages.extend(init_pdf.pages)
        new_pdf.save(str(pdfFile))

    def totalPageNr(file):
        ppdf = pikepdf.open(file)
        return len(ppdf.pages)
    
    def mergePdfs(pdfFiles, outputFileName= 'merged'):
        if(not outputFileName.endswith(".pdf")):
            outputFileName += '.pdf'
        pdf = Pdf.new()
        for file in pdfFiles:
            src = Pdf.open(file)
            pdf.pages.extend(src.pages)

        pdf.save(outputFileName)
        
    def pdf2yamlMapper(pdfName):
        dirname = os.path.dirname(pdfName)
        pdfName = os.path.basename(pdfName)[:-4]
        yamls = Path.filesWithExtension("yaml", dirname)
        for y in yamls:
            if(pdfName == os.path.basename(y).replace(".yaml","")):
                return y
        print("Not found")
        return ''
    
    def displayInNotebook(filePath):
        import base64
        from IPython.display import HTML
        class Temp:
            def chunk_24_read(pdf_filename) :
                with open(pdf_filename,"rb") as f:
                    byte = f.read(3)
                    while(byte) :
                        yield  byte
                        byte = f.read(3)

            def pdf_encode(pdf_filename):
                encoded = ""
                length = 0
                for data in Temp.chunk_24_read(pdf_filename):
                    for char in base64.b64encode(data) :
                        if(length  and  length % 76 == 0):
                           encoded += "\n"
                           length = 0

                        encoded += chr(char)  
                        length += 1
                return encoded
        return HTML(f"""
                        <iframe src="data:application/pdf;base64,{Temp.pdf_encode(filePath)}#page=2" width="100%" height="400">
                    """)

    def readPdf(pdf):
        yamlFile = PDF.pdf2yamlMapper(pdf)
        if( yamlFile != ''):
            return PDF.loadPdfFromText(yamlFile)
        else:
            return PDF.getTextFromPDF(pdf)

    def extractPdf(inputPdfName, outPdfName, _range):
        x,y = _range
        dst = Pdf.new()
        p = WidgetsDB.progressBar(y-x)
        with Pdf.open(inputPdfName) as pdf:
            for i in range(x-1,y-1):
                p.value += 1
                dst.pages.append(pdf.pages[i])
        dst.save(outPdfName)

    def getPdfPageAsImage(pdfPath, pageNr):
        from useful.CryptsDB import CryptsDB
        from useful.Path import Path
        from useful.LibsDB import LibsDB
        import os
        tempPdf = CryptsDB.generateRandomName(20) + ".pdf"
        PDF.extractPdf(pdfPath, tempPdf, (pageNr-1,pageNr))
        PDFTOPPMPATH = LibsDB.cloudPath() + r"\global\code\libs\poppler-0.68.0\bin\pdftoppm.exe"
        outFilename = Path.joinPath(os.path.dirname(pdfPath), CryptsDB.generateRandomName(20))
        print('"%s" -png "%s" "%s"' % (PDFTOPPMPATH, tempPdf, outFilename))
        os.system('"%s" -png "%s" "%s"' % (PDFTOPPMPATH, tempPdf, outFilename))
        Path.delete([tempPdf])

    def rotatePdf(path, angle = 90, outPath = ''):
        if(outPath == ''):
            outPath = 'rotated.pdf'
        my_pdf = pikepdf.Pdf.open(path)
        for page in my_pdf.pages:
            page.Rotate = angle
        my_pdf.save(outPath)
        
    def searchInPdfsList(pdfs, word):
        from useful.SearchSystem import PdfSearchEngine
        from useful.Database import Database
        db = PdfSearchEngine(pdfs)
        return Database.dbSearch(db, word)
        