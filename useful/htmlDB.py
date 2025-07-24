import urllib.request
from bs4 import BeautifulSoup, NavigableString, Tag
import collections

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
        import requests
        r = requests.get(link, stream = True)
        with open(name,"wb") as pdf: 
            for chunk in r.iter_content(chunk_size=1024):
                if (chunk): 
                    pdf.write(chunk)
    
    def getTags(name, soup):
        return soup.findAll(name)

    def searchOnSoup(dic, soup):
        """
        dic: {"tagName":"name", "attr":{"attrName": "attrValue"}}
        """
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
        import requests
        import json
        r = requests.get(link)
        jsonData = json.loads(r.text)
        return jsonData
    def bfs_soup(soup_node, max_layer=None, ignoreRoot = False):
        """
        Performs a Breadth-First Search (BFS) on a Beautiful Soup parse tree.

        Yields nodes (Tag or NavigableString) layer by layer.

        Args:
            soup_node (BeautifulSoup or Tag): The starting node for the BFS.
                                            This can be the root BeautifulSoup object
                                            or any specific Tag within the tree.
            max_layer (int, optional): The maximum layer (depth) to traverse.
                                       - Layer 0 is the starting `soup_node` itself.
                                       - Layer 1 includes its direct children.
                                       - If None, the search will traverse the entire tree.
                                       The function will yield nodes UP TO and INCLUDING
                                       the max_layer, but will not add children of nodes
                                       at max_layer to the queue.

        Yields:
            BeautifulSoup or Tag or NavigableString: The nodes encountered during BFS.
        """
        if not isinstance(soup_node, (BeautifulSoup, Tag, NavigableString)):
            raise TypeError("soup_node must be a BeautifulSoup, Tag, or NavigableString object.")

        queue = collections.deque([(soup_node, 0)])
        isRoot = True
        while queue:
            current_node, current_layer = queue.popleft()
            if isRoot and ignoreRoot:
                isRoot = False
                pass
            else:
                yield current_node

            # If max_layer is specified and we've reached or exceeded it,
            # we do not add children of this node to the queue.
            if max_layer is not None and current_layer >= max_layer:
                continue # Move to the next item in the queue

            # Add children to the queue if the current_node can have children
            # (i.e., it's a BeautifulSoup object or a Tag)
            # and we haven't hit the max_layer.
            if hasattr(current_node, 'contents'):
                for child in current_node.contents:
                    # Beautiful Soup sometimes includes empty strings for whitespace,
                    # which aren't typically what you want to process as a "node".
                    # You might want to filter these or include them based on your needs.
                    # Here, we'll filter out purely whitespace strings.
                    if isinstance(child, NavigableString) and not child.strip():
                        continue
                    
                    # If it's a Tag or a non-empty NavigableString, add it to the queue
                    queue.append((child, current_layer + 1))
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