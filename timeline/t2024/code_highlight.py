from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum
from useful.basic import Main as ObjMaker
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
import ipyreact
import os
import pathlib
from LibPath import getPath

class ReactHighlightCode(ipyreact.ValueWidget):
    _esm = pathlib.Path(os.sep.join([getPath(), "javascript", "2024", "Highlight.js"]))
def CodeHighlighter():
    container = Utils.container([Utils.get_comp(dict(value="set code"), IpywidgetsComponentsEnum.Label)])
    def highlight_code_with_line_numbers(code, lexer):
        formatter = HtmlFormatter(linenos=True, style='default')
        highlighted_code = highlight(code, lexer, formatter)
        css = formatter.get_style_defs()
        comp = ReactHighlightCode(value= {"code":highlighted_code, "css": css})
        comp.add_class("overflow-auto")
        rapper = Utils.wrapper(comp)
        container.pop()
        container.append(rapper)
    def set_content(content, lang = "python"):
        lexer = get_lexer_by_name(lang, stripall=True)
        s.process.content = content
        highlight_code_with_line_numbers(content, lexer)
    s = ObjMaker.uisOrganize(locals())
    return s