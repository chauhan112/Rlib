from SystemInfo import SystemInfo
import os

class ICopy:
  def copy(self, txt):
    raise NotImplementedError('abstract method')

class IPaste:
    def get(self):
        raise NotImplementedError('abstract method')

class WindowCopy(ICopy):
  def copy(self,txt):
    import pyperclip
    pyperclip.copy(txt)

class DefaultCopy(ICopy):
    def copy(self, text):
        from LibPath import computerName
        dflts = {
            'mobileTermux' : TermuxCopy(),
            'home' : WindowCopy(),
            'office': WindowCopy(),
            'linux' : LinuxCopy(),
            'windows' : WindowCopy()
        }
        dflts[computerName()].copy(text)

class TermuxClipText(IPaste):
    def get(self):
        return os.system(f'termux-clipboard-get')

class DefaultPaste(IPaste):
    def get(self):
        from LibPath import computerName
        dflts = {
            'mobileTermux': TermuxClipText()
        }
        name = computerName()
        if name in dflts:
            return dflts[name].get()
            
        import pyperclip
        return pyperclip.paste()

class LinuxCopy(ICopy):
  def copy(self,txt):
    os.system("echo '{}' | xclip -selection clipboard".format(txt))
    
class TermuxCopy(ICopy):
  def copy(self,txt):
    os.system(f'termux-clipboard-set "{txt}"')

class ClipboardDB:
    def copy2clipboard(content, copy_sys:ICopy = DefaultCopy()):
        copy_sys.copy(content)
    
    def clipboardImage2Pdf( name = ''):
        from Path import Path
        imgPath = ClipboardDB.saveImage()
        image.save(imgPath)
        pdfName = name+".pdf"
        images2pdf(imgPath, pdfName)
        Path.delete([imgPath])
        return pdfName
    
    def saveImage(name=""):
        from CryptsDB import CryptsDB
        if(name ==""):
            name = CryptsDB.generateRandomName(20) + ".png"
        image = ClipboardDB.getImage()
        image.save(name)
        return name

    def getImage():
        from PIL import ImageGrab
        im = ImageGrab.grabclipboard()
        if(im is None):
            raise IOError("No image in clipboard")
        return im
    
    def imageText():
        from Path import Path
        from ImageProcessing import ImageProcessing as im
        name = ClipboardDB.saveImage()
        text = im.image2text(name)
        Path.delete([name])
        return text

    def getText(paster : IPaste = DefaultPaste()):
        return paster.get()
        
    def displayCode(name = "python"):
        from ModuleDB import ModuleDB
        return ModuleDB.colorPrint(name, ClipboardDB.getText())