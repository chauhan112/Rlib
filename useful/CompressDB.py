import zlib
import base64
import os
import gzip

class CompressDB:
    def content():
        class Temp:
            def compressToBinVal(content):
                return gzip.compress(content)

            def decompressFromBinVal(content):
                return gzip.decompress(content)
            
            def decode_base64_and_inflate( b64string ):
                decoded_data = base64.b64decode( b64string )
                return zlib.decompress( decoded_data , -15).decode("utf-8")

            def deflate_and_base64_encode( string_val ):
                zlibbed_str = zlib.compress( string_val )
                compressed_string = zlibbed_str[2:-4]
                return base64.b64encode( compressed_string )
        return Temp
    
    def files():
        from SerializationDB import SerializationDB
        class Cmp:
            def compress(self, files, outputFile):
                k = _PackCompressedFile(files)
                SerializationDB.pickleOut(k, outputFile)
            
            def decompress(self, filename):
                a = SerializationDB.readPickle(filename)
                a.decompressAll()
        return Cmp()

class _PackCompressedFile:
    def __init__(self, files):
        self.files = {os.path.basename(file): self.compress(self.readFileAsBin(file)) for file in files}
    
    def readFileAsBin(self, filepath):
        with open(filepath, "rb") as f:
            return f.read()
        
    def compress(self, contentAsBin):
        return gzip.compress(contentAsBin)
    
    def addNewFile(self, filePath, folder = None):
        name = os.path.basename(filePath)
        if(name in self.files and folder is None):
            print("fileName already exists. Specify folder name to keep in separate folder")
            return 
        
        if(folder is not None):
            name = folder +os.sep +name
        
        self.files[name] = self.compress(self.readFileAsBin(filePath))
        
    def decompress(self, name):
        self.writeFileWithContent(name, self.files[name])
    
    def decompressAll(self):
        for file in self.files:
            self.decompress(file)

    def writeFileWithContent(self, name, contentAsBin):
        from FileDatabase import File
        File.createFileInsideNonExistingFolder(name, contentAsBin, ty= "wb")
        
    def getFileNames(self):
        return list(self.files.keys())
