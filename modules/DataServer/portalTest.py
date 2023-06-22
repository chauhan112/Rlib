def gitPortalTest():
    from modules.DataServer.Git import GitPortal, GitContact
    from modules.DataServer.Tools import GitPortalInstantiate
    from modules.DataServer.Interfaces import IContact
    path1, path2 = r'..\p1123123', r'..\p223231'
    p1 = GitPortal(GitPortalInstantiate(path1).execute())
    p2 = GitPortal(GitPortalInstantiate(path2).execute())

    server = GitContact("server")
    p1Con = GitContact('p1')
    p2Con = GitContact('p2')
    p1.sendMessage('hi there', p2Con)
    print(p2.receiveMessage(p2Con))
    import os
    os.system(f"rm -rf {path1}")
    os.system(f"rm -rf {path2}")

def pathPortalTest():
    from modules.DataServer.Portals import PathPortal
    from modules.DataServer.Interfaces import NameContact
    c1, c2  = NameContact("c1"), NameContact("c2")
    commonPath = "path_test"
    p1 = PathPortal(commonPath)
    p2 = PathPortal(commonPath)
    p1.sendMessage('hi there', c2)
    print(p2.receiveMessage(c2))
    import os
    os.system(f'rm -rf {commonPath}')
# from LibPath import insertPath
# insertPath()
# pathPortalTest()