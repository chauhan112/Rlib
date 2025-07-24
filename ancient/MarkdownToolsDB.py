from IPython.display import display,Markdown
from useful.ListDB import ListDB


class MarkdownToolsDB:
    dic = {
        "Ax": 'A\\overrightarrow{x}',
        "Ax_b": "A\\overrightarrow{x} = \\overrightarrow{b}",
        "normal_equations": "A^{\\top}A\\overrightarrow{x} = A^{\\top}\\overrightarrow{b}",
        "equi": "\\equiv",
        "epsilon": "\\varepsilon",
        "pipe": "\\Vert",
        "transpose":"\\top",
        "infinity": "\\infty",
        "rightarrow": "\\rightarrow",
        "real number R": "\\rm I\!R",
        "belongs in": "\\in",
        "A.T.A": "A^{\\top} A",
        "subset": "\\subset"
    }
    def list2htmlOrderedList(arr, ordered = True):
        lists = [f"<li>{val}</li>" for val in arr]
        k = ""
        if(ordered):
            k = "<ol>"+ "".join(lists)+"</ol>"
        else:
            k = "<ul>"+ "".join(lists)+"</ul>"
            
        from ancient.ClipboardDB import ClipboardDB
        ClipboardDB.copy2clipboard(k)
        return k
    
    def integrate(strA, strB, strExp):
        # latex tools
        k = f"\\int_{{{strA}}}^{{{strB}}} {strExp} d x"
        return k

    def frac(nomi, deno):
        k = f" \\frac{{{nomi}}}{{{deno}}}"
        return k

    def vector(string):
        k = f"\\overrightarrow{{{string}}}"
        return k

    def partial(var, dis = True):
        k = f"\\partial {{{var}}}"
        return k

    def matrix(expArr):
        if(len(expArr) == 0):
            return 

        if(len(expArr) > 50):
            print("Array too big. Takes alot of time to render")
            print("print normally")
            print(expArr)
            return
        colsNr = len(expArr[0])
        arr = []
        for row in expArr:
            newRow = " & ".join([str(i) for i in row])
            arr.append(newRow)
        exp = " \\\\\n".join(arr)
        lls = "l"* colsNr
        k = f"\left[\\begin{{array}}{{{lls}}}"
        k += "\n" +  exp + "\n"
        k += "\\end{array}\\right]"
        return k
    
    def sub(val, subs):
        return f"{val}_{{{subs}}}"
    def sup(val, sups):
        return f"{val}^{{{sups}}}"
    def joiner(*arr):
        return " ".join(arr)
    def dash(val):
        return f"(val)^{{\\prime}}"
    def hat(val):
        return f"\\widehat{{{val}}}"
    def dispjoin(*arr):
        display(Markdown(f"$${MarkdownToolsDB.joiner(*arr)}$$"))
    def tilde(val):
        return f"\\widetilde{{{val}}}"
    def norm(val):
        pipe = MarkdownToolsDB.dic['pipe']
        return MarkdownToolsDB.brace(val, lr = pipe)
    def search(word):
        from useful.Database import Database
        return Database.dicDB(MarkdownToolsDB.dic)

    def limit(var, tends2):
        return f"\\lim _{{{var} \\rightarrow {tends2}}}"
    def summation(bottom, top, functExp = ""):
        return f"\\sum_{{{bottom}}}^{{{top}}} {functExp}"
    def Ax_b(x="x",b ="b" ):
        return f'A\\overrightarrow{{{x}}} = \\overrightarrow{{{b}}}'
    
    def minMaxBelow(mainText, belowText):
        return f"\\{mainText}_{{{belowText}}}"
    
    def brace(exp, l= "(", r=")", lr =""):
        if(lr != ""):
            l = lr
            r = lr
        return f"{l}{exp}{r}"