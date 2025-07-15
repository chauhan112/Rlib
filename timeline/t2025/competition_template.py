

def lm(f,arr):
    return list(map(f,arr))
def fsl(f):
    return xsl(x,input())
def xsl(f,p):
    return lm(f, p.split())
def fnl(n):
    return lm(lambda x: input(), range(n))
# if __name__ == '__main__':
#     a = int(input())