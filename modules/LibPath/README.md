# CPP ProjectFile
This package is like database for the cpp project. It helps in searching sepecific parts of codes like variables and string. It is written in python. It can open  the code in editor for with openFile methods
----

# Installation 
`python setup.py install`

# Demos
```python
path = r"C:\Users\rajac\Desktop\Working\Git\MICpad"
mic = CppProject(path = path)

mic.summarize()

mic.searching("variable", case=False)
```