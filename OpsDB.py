class IOps:
    def execute(self):
        raise NotImplementedError('abstract method')

class IGroupIdentifier:
    def analyse(self, element):
        raise NotImplementedError('abstract method')

class OpsDB:
    def group(container, groupingFunc, resappeder = lambda x: x):
        gr = {}
        for ele in container:
            groupKey = groupingFunc(ele)
            if(groupKey not in gr):
                gr[groupKey] = []
            gr[groupKey].append(resappeder(ele))
        return gr
        
    def grouperValues(mapFunction, contentList, operationOnValue = None):
        g = {}
        for row in contentList:
            opsVal = row
            if(operationOnValue is not None):
                opsVal = operationOnValue(row)
            l = mapFunction(row)
            try:
                g[l].append(opsVal)
            except:
                g[l] = [opsVal]
        return g

    def mapper(leftList, rightList, mappingCondition, one2one = True):
        dic = {}
        for l in leftList:
            for r in rightList:
                if(mappingCondition(l,r)):
                    if(one2one):
                        dic[l] = r
                        break
                    else:
                        try:
                            dic[l].append(r)
                        except:
                            dic[l] = r
        return dic
    
    def list2TreeMapperIter(links):  
        mapped = {}
        for val in links:
            if(len(val) != 2):
                try:
                    mapped[val[0]]['folders'].append(val[1:])
                except:
                    try:
                        mapped[val[0]]['folders'] = [val[1:]]
                    except:
                        mapped[val[0]] = {}
                        mapped[val[0]]['folders'] = [val[1:]]
            else:
                try:
                    mapped[val[0]]['files'].append(val[1])
                except:
                    try:
                        mapped[val[0]]['files'] = [val[1]]
                    except:
                        mapped[val[0]] = {}
                        mapped[val[0]]['files'] = [val[1]]
        return mapped

    def grouperBasedOnKeys(mapperKey,vals, mapperValue = lambda x: x ):
        dic = {}
        for val in vals:
            key = mapperKey(dic, val)
            if(key is None):
                key = mapperValue(val)
            try:
                dic[key].append(val[0])
            except:
                dic[key] = [val[0]]
        return dic
    
    def linearGroup(condition, container, ini = 0):
        glueingType = [0]
        glueVal = 0
        for i in range(0 + ini,len(container)-1 + ini):
            b = container[i+1]
            a = container[i]
            if (condition(a,b)):
                glueVal += 1
            glueingType.append(glueVal)
        return glueingType
    
    def groupKeys(mappingFunc, contentList):
        g = {}
        for i,element in enumerate(contentList):
            l = mappingFunc(element)
            try:
                g[l].append(i)
            except:
                g[l] = [i]
        return g

    def mapDictionary(func, dic):
        newDic = {}
        for key in dic:
            newDic[key] = func(dic[key])
        return newDic

    def fillGroup(group, container):
        g = {}
        for key in group:
            g[key] = []
            for index in group[key]:
                g[key].append(container[index])
        return g

    def cmd():
        class Cmds:
            def onthread(commands = ['start']):
                if(type(commands) ==str):
                    commands = [commands]
                OpsDB.runOnThread(Cmds.run, [commands])
            def run(commands = ['start'], getErr = False):
                if(type(commands) ==str):
                    commands = [commands]
                import subprocess
                command = " && ".join(commands)
                proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stderr= subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                out, err = proc.communicate()
                out = out.decode("ascii")
                err = err.decode("ascii")
                if(getErr):
                    return out, err
                return out
            def atPath(path):
                import os
                twoLetters = os.path.abspath(path)[:2]
                cmds = [twoLetters,f'cd "{path}"', 'start'] 
                OpsDB.cmd().onthread(cmds)
                
        return Cmds

    def runOnThread(func, params = ()):
        import threading
        k = threading.Thread(target=func, args = params, daemon=True)
        k.start()
        return k