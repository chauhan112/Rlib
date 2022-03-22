import urllib.request
from bs4 import BeautifulSoup
import requests


class htmlDB:
    def getHtmlFromUrl(link):
        fp = urllib.request.urlopen(link)
        mybytes = fp.read()

        htmlContent = mybytes.decode("utf8")
        fp.close()
        return htmlContent

    def getParsedData(pageContent, parser = 'html.parser'):
        return BeautifulSoup(pageContent, parser)

    def getAttrIndex(tag, attr):
        return tag[attr]
    
    def downloadPdf(link, name):
        r = requests.get(link, stream = True)
        with open(name,"wb") as pdf: 
            for chunk in r.iter_content(chunk_size=1024):
                if (chunk): 
                    pdf.write(chunk)
    
    def getTags(name, soup):
        return soup.findAll(name)

    def searchOnSoup(dic, soup):
        if(not('tagName' in dic and 'attr' in dic)):
            print('give dictionary containing {"tagName":"name", "attr":{"attrName": "attrValue"}}')
            return
        return soup.findAll(dic['tagName'], dic["attr"])

    def urlDecode(value):
        import urllib.parse
        return urllib.parse.unquote(value)
        
    def urlEncode(value):
        import urllib.parse
        return urllib.parse.quote(value)

    def htmlDecode(value):
        import html
        return html.unescape(value)

    def displayTableFromArray(arr, displayIt = True):
        from IPython.display import HTML, display
        arrHtmlTxt = "".join([f"<th>{head}</th>\n  " for head in arr[0]])
        arrHtmlTxt = f"<tr>{arrHtmlTxt}</tr>\n"
        for row in arr[1:]:
            vals = ""
            for val in row:
                vals += f"<td>{val}</td>\n  "
            arrHtmlTxt += f"<tr>{vals}</tr>\n"
        if(displayIt):
            display(HTML(f"<table>{arrHtmlTxt}</table>"))
            return
        return f"<table>{arrHtmlTxt}</table>"

    def fetchApiResults(link):
        import json
        r = requests.get(link)
        jsonData = json.loads(r.text)
        return jsonData
    
class HtmlCssJavascript:
    def calender():
        from IPython.display import HTML
        return HTML('<input type="date">')
        
    def valuePairDisplay(dic):
        content = ""
        for key in dic:
            content += f'<div class ="row"><span class="key">{key} ::</span> <span class="value">{dic[key]}</span> </div>'
        content = f'<div class="container"> {content}</div>'
        return content
    
    def getDiv(content):
        return f"<div>{content} </div>"

    def getTextArea(content):
        return f"<textarea>{content} </textarea>"

    def horizontalBox(contentList):
        k = "<div style='width:100%;display:flex;'>"
        for val in contentList:
            k += " <div style='float: left; margin:5px;'>" + val + "</div>"
        k += "</div>"
        return k