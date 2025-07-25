import nbformat as nbf
from useful.FileDatabase import File
import os
class NotebookDB:
    id_ = None
    def getCellsOfnoteBook(nb):
        cells = nbf.reads(File.getFileContent(nb),4)['cells']
        return cells

    def getCodeCellContent(nb):
        cells = NotebookDB.getCellsOfnoteBook(nb)
        contents = [cell['source'] for cell in cells if cell['cell_type'] == 'code' and cell['source'].strip() != ""]
        return contents

    def notebookJsonContentsWithCells(cellContents):
        def getNewCell(content, typ = "code"):
            if(typ in ["code", "py", ""]):
                return nbf.v4.new_code_cell(content)
            return nbf.v4.new_markdown_cell(content)
        nb = nbf.v4.new_notebook()
        cells = [getNewCell(content,typ) for typ, content in cellContents]
        nb['cells'] = cells
        return nbf.writes(nb)
    def nbCreate(name, codes, markdowns):
        lines = [("code", c) for c in codes]
        for i, c in markdowns:
            lines.insert(i, ("md",c))
        NotebookDB.createNotebookWithCells(name, lines)

    def convertNotebook(notebookPath, outOutFilename = None):
        from nbconvert import PythonExporter
        from useful.Path import Path

        if(outOutFilename is None):
            outOutFilename = os.path.basename(notebookPath)[:-5] + 'py'
        modulePath = outOutFilename

        with open(notebookPath) as fh:
            nb = nbf.reads(fh.read(), nbf.NO_CONVERT)
        exporter = PythonExporter()
        source, meta = exporter.from_notebook_node(nb)
        with open(modulePath, 'w+') as fh:
            fh.writelines(source)

    def createNotebookOfAllRunCells(name, _ih):
        import nbformat as nbf
        nb = nbf.v4.new_notebook()
        cells = [NotebookDB.getNewCell(content,"code") for content in _ih]

        nb['cells'] = cells
        if(not name.endswith(".ipynb")):
            name += '.ipynb'

        with open(name, 'w') as f:
            nbf.write(nb, f)

    def summarizeTheCoding(_ih):
        from useful.SerializationDB import SerializationDB
        import os
        device, id_ = NotebookDB.getSummaryInfos()
        ouputFile = NotebookDB.outFilename()
        if(os.path.exists(ouputFile)):
            log = SerializationDB.readPickle(ouputFile)
        else:
            log = {}
        if(device not in log):
            log[device]= {}
        log[device][id_] = _ih
        SerializationDB.pickleOut(log, ouputFile)

    def getSummaryInfos():
        from useful.ModuleDB import ModuleDB
        from useful.CryptsDB import CryptsDB
        device = ModuleDB.laptopName()
        if(NotebookDB.id_ is None):
            NotebookDB.id_ = CryptsDB.generateUniqueId()
        id_ = NotebookDB.id_
        return device, id_

    def outFilename(date = None):
        from useful.TimeDB import TimeDB
        import os
        from LibPath import dumperPath
        import datetime

        fileName = ".".join(TimeDB.getTimeStamp(date).split(", ")[::-1]).replace(".", "_") + '.pkl'
        yearPath = os.sep.join([dumperPath(), f'{datetime.datetime.now().year}'])
        filePath = os.sep.join([yearPath, fileName])
        return filePath
