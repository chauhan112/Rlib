
def createFolderStructureTest():
    strcu = {'folders': {'LYXhN': {'folders': {'nFxDW': {'folders': {},
         'files': ['NQgcP.py']}},
       'files': []},
      'SYYS8': {'folders': {}, 'files': ['IP7nt.java']},
      'ZEfJi': {'folders': {'5YpQa': {'folders': {'QYfnK': {'folders': {},
           'files': ['oIspA.cpp']}},
         'files': []}},
       'files': []},
      'rkXEZ': {'folders': {'raNTh': {'folders': {}, 'files': ['BooHe.txt']}},
       'files': []}},
     'files': ['Evqa5.java']}
    import os
    createFolderStruc(strcu, "test")
    def doesExist(path):
        assert os.path.exists(path)
    