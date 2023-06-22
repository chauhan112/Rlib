class PhotoLogger:
    def __init__(self, reader):
        self.reader = reader
    def listPhotos(self):
        content = self.reader.readAll()
        for i, val in enumerate(content):
            print(f"{i+1}. {val}")
    def openPhoto(self):
        pass
    def cmdRunner(self):
        dic = {
            'listPhotos': None,
            'add': None,
            'search' : None
        }
    def adder(self):
        res = []
        while True:
            inp = input("name: ").strip()
            if inp == ":q":
                break
            res.append(inp)
        return res
    def save(self, name, results):
        cont = self.reader.readAll()
        if name in cont:
            cont = cont[name]
        else:
            cont = set([])
        for val in results:
            cont.add(val)
        self.reader.add(name, cont, overwrite= True)
    def search(self, word, case = False, reg= False):
        from ComparerDB import ComparerDB
        content = self.reader.readAll()
        res = []
        for ph in content:
            for val in content[ph]:
                if ComparerDB.has(word, val, case, reg):
                    res.append(ph)
        return res