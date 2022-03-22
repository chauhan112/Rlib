class StaticDisplayerManager:
    vals = {'UrlDB container size Info' : {'count': 0, 'checker': lambda x: x % 5 == 0},
        'total modules file number' : {'count': 0, 'checker': lambda x: x % 10 == 5}}
    
    def display(key, val):
        try:
            StaticDisplayerManager.vals[key]['count'] += 1
            if(StaticDisplayerManager.vals[key]['checker'](StaticDisplayerManager.vals[key]['count'])):
                print(val)
        except:
            pass