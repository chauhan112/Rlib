import os

class TestDB:
    def iterativeJacobiTest():
        from NumericalAnalysis import NumericalAnalysis as na
        k = na.jacobiInterativeSolution([lambda x: 0.5 -1.5* x, lambda x: (5 + x)/4],[0,0], 100) == [-1.0, 1.0]
        print(k)

    def pickleTest():
        from CryptsDB import CryptsDB
        from SerializationDB import SerializationDB
        data = {"a": "somtezh"}
        name = CryptsDB.generateRandomName()
        SerializationDB.pickleOut(data, name)
        if(SerializationDB.readPickle(name) == data):
            print('pickle test passed')
        
    def reListTest():
        from ListDB import ListDB
        inp = ['2. app to generate data about bought stuffs',
            '3. clothes management app',
            '4. tree structure to diagram']

        out = ['1. app to generate data about bought stuffs',
            '2. clothes management app',
            '3. tree structure to diagram']
        assert(ListDB.reList(inp, False) == out)


    def combinerTest():
        from StaggingAreaDB import StaggingAreaDB
        from MathObjectDB import OpenRange
        testCases = {
            'input': {
                'l1': [OpenRange(0,3), OpenRange(3, 4), OpenRange(4, 7), OpenRange(8, 9), OpenRange(9, 12)],
                'l2': [OpenRange(3,7)]
            },
            'output': [OpenRange(0,3), OpenRange(3, 7), OpenRange(8,9), OpenRange(9,12)] # (3, 7) intersects (3, 4) and (4, 7), so they are replaced by (3, 7)
        }

        res1 = StaggingAreaDB.combiner().combiner(testCases['input']['l1'],testCases['input']['l2'])
        res2 = StaggingAreaDB.combiner().combiner2(testCases['input']['l1'],testCases['input']['l2'])
        assert [str(i) for i in res1] == [str(i) for i in testCases['output']] , 'failed'
        assert [str(i) for i in res2] == [str(i) for i in testCases['output']] , 'failed'
        
    def add2DicTest():
        from ListDB import ListDB
        dic = {'key1': {'key11': 'val11'}, 'key2': {'key21': {'key211': 'val211'}}}
        location = ['key2', 'key21', 'key212']
        val = 'val212'
        dicOut = {'key1': {'key11': 'val11'}, 'key2': {'key21': {'key211': 'val211', 'key212':'val212'}}}
        ListDB.dicOps().add(dic,  location,val)
        assert(dic == dicOut)
    
    def branchPathTest():
        from ListDB import ListDB
        dic1 = {'a': {'aa':'val', 'bb': {'aaa': 'val', 'aab': {'aaba': 1, 'aabb': 2}}}, 'b': 4}
        dic2 = {'a': 1, 'b': 4, 'c': 5}
        res1 = [['a','aa'],['a','bb','aaa'], ['a','bb','aab', 'aaba'],['a','bb','aab', 'aabb'], ['b']]
        res2 = [['a'], ['b'], ['c']]
        assert ListDB.branchPath(dic1) == res1
        assert ListDB.branchPath(dic2) == dic2
        
    def dicFlattenTest():
        from ListDB import ListDB
        inp = {'a':{'b':{'c': 's','d':'a'}, "p":'m'},'k':'kl'}
        out = {'c': 's', 'd': 'a', 'p': 'm', 'k': 'kl'}
        assert(ListDB.dicOps().flatten(inp) == out)
        inp2 = {'on startup': {'mount google sync': 'google-drive-ocamlfuse ~/GDrive'},
                 'common commands': {'show seconds on clock': 'gsettings set org.gnome.shell.clock show-seconds true'}}
        out2 = {'mount google sync': 'google-drive-ocamlfuse ~/GDrive',
                 'show seconds on clock': 'gsettings set org.gnome.shell.clock show-seconds true'}
        assert(ListDB.dicOps().flatten(inp2) == out2)
    
    def replaceTest():
        from RegexDB import RegexDB
        inp = """+ sizeHint() const: QSize
    + updateRecentMenu():"""
        reg = "(?<=\\+ ).*(?=\\()"
        out = """+ <font face='comic sans ms' color ='GoldenRod'>sizeHint</font>() const: QSize
    + <font face='comic sans ms' color ='GoldenRod'>updateRecentMenu</font>():"""
        func = lambda x: f"<font face='comic sans ms' color ='GoldenRod'>{x}</font>"
        assert(RegexDB.replace(reg, inp, func) == out)
        
    def openNotebooktTest():
        from jupyterDB import jupyterDB
        inp = r"D:\cloud\timeline\fifth semester\praxis bericht\ops\latex"
        # expected output is printed url which can be clicked to open 
        jupyterDB.localIpyLink(inp)
    
    def replaceTest2():
        from WordDB import WordDB
        class WordReplaceTest:
            def withFuncTest():
                inp = "Ram has brought his laptop."
                def rplF(wordInfo):
                    strt, end, word = wordInfo
                    dic = {"Ram": "Sita", "his": "her"}
                    try:
                        return dic[word]
                    except:
                        return word
                exp_out = "Sita has brought her laptop."
                reg = "(Ram|his)"
                out = WordDB.replace().withFunc(reg, rplF, inp)
                assert(replace().withFunc(reg, rplF, inp) == exp_out)

            def withContainersTest():
                inp = "timehere timehere timehere, timehere"
                reg = "timehere"
                continer = ["Sunday", "Monday", "Tuesday"]
                exp_out = "Sunday Monday Tuesday, Sunday"
                out = WordDB.replace().withContainers(reg,continer, inp)
                print(out)
                assert( out == exp_out)
                
            def oneAfterAnotherTest():
                inp = "cat parrot pigeon"
                rpltuple = [("cat", "tiger"), ("parrot", "shark")]
                exp_out = "tiger shark pigeon"
                out = WordDB.replace().oneAfterAnother(inp, rpltuple)
                print(out)
                assert(out == exp_out)
        return WordReplaceTest
        
    def TestPickleWriter(Writer):
        path = "test.pkl"
        if(os.path.exists(path)):
            os.remove(path)
        write = Writer(path)
        write.add("today", "testing")
        val = write.read("today")
        assert val == "testing"
        write.delete("today")
        assert write.readAll() == {}
        
        write.add(["TODAY", "12pi"], "asdns")
        assert write.read("TODAY") == {'12pi': "asdns"}
        assert write.read(["TODAY", "12pi"]) == 'asdns'
        write.add(["TODAY", "12pi"], "cmmi", True)
        assert write.read(["TODAY", "12pi"]) == 'cmmi'
        assert write.readAll() == {"TODAY":{'12pi':'cmmi'}}
        
        write.delete("TODAY")
        assert write.readAll() == {}
        
    def test_ast_uses():
        import ast
        from modules.code_parser.ast_parser import Uses
        code = ['def sdk(pas =sjfn()):', '    class Tem(ALL()):', '        def hi():', '            q()', '    ',
                'class ABC:', '    pass']
        code = "\n".join(code)
        exp = [('q',), ('ALL',), ('sjfn',)]
        
        us = Uses()
        us.setData(ast.parse(code))
        assert set(us.get()) == set(exp), 'faild'
    def dicDeleteTest():
        from ListDB import ListDB
        dic = {"a": 1, 'b':{'c, d': 2}}
        loc = ['b', 'c, d']
        ListDB.dicOps().delete(dic, loc)
        assert dic == {'a': 1, 'b': {}}
        
    def depth_calc_test():
        from ListDB import ListDB
        a = {}
        a2 = {'1':2}
        a3 = {1:{2:{3:4}}}
        assert ListDB.dicOps().depth_calculator(a) == 0
        assert ListDB.dicOps().depth_calculator(a2) == 1
        assert ListDB.dicOps().depth_calculator(a3) == 3
        
class JupyterDBCodeDumper:
    def test_dumper_path():
        from jupyterDB import jupyterDB
        foldername = os.path.basename(jupyterDB.codeDumper()._dumper_path)
        assert foldername == "daily code dumper"
        