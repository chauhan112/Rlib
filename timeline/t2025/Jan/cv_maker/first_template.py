from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
from useful.basic import Main as ObjMaker
import os
import subprocess
from useful.basic import Main as ObjMaker
from timeline.t2023.dep_extractor.dependency_extractor import DicOps
from SerializationDB import SerializationDB
from LibsDB import LibsDB

def makePdf(texContent, outputPath= None):
    if outputPath is None:
        outputPath = ".cv-output/main.pdf"
    if not outputPath.endswith(".pdf"):
        outputPath += "/main.pdf"
    dn = os.path.dirname(outputPath)
    fn = os.path.basename(outputPath)
    tx = ".".join(fn.split(".")[:-1]) + ".tex"
    if not os.path.exists(dn):
        os.makedirs(dn)
    texFile = os.sep.join([dn, tx])
    File.overWrite(texFile, texContent)
    subprocess.call(f'cd "{dn}" && pdflatex "{tx}"', shell=True)
    return outputPath
def Template1():
    def getWorkExperience(arr):
        txtArr = []
        for exp in arr:
            res = r"\begin{tabularx}{0.97\linewidth}{>{\raggedleft\scshape}p{2cm}X}" + "\n"
            period, employer, jobTitle,des, kvs= exp
            _from, till = period
            name, loc = employer
            res += r"\gray Period & \textbf{"+ _from + " --- " + till + r"}\\"+ "\n"
            res += r"\gray Employer & \textbf{"+ name + r"} \hfill "+ loc+r"\\"+ "\n"
            res += r"\gray Job Title & \textbf{" + jobTitle+r"}\\"+ "\n"
            for k in kvs:
                v = kvs[k]
                res += r"\gray "+ k +r" & \textbf{"+ v +r"}\\"+ "\n"
            res += "       & " + des+ "\n"
            res += r"\end{tabularx}"+ "\n"
            txtArr.append(res)
        return "\n\\vspace{12pt}\n\n".join(txtArr)
    def get_education(arr):
        rt = []
        for ed in arr:
            period, degree, note, university, des = ed
            res = r"\begin{tabularx}{0.97\linewidth}{>{\raggedleft\scshape}p{2cm}X}" + "\n"
            f, t = period
            res += f"\\gray Period & \\textbf{{{f} --- {t}}}\\\\\n"
            res += f"\\gray Degree & \\textbf{{{degree}}}\\\\" + "\n"
            res += r"\gray Note & \textbf{<note>}\\".replace("<note>", note)  + "\n"
            name, loc = university
            res += r"\gray University & \textbf{<Uni>} \hfill <loc>\\".replace("<Uni>",name).replace("<loc>", loc)  + "\n"
            res += "       & " + des+ "\n"
            res += r"\end{tabularx}"+ "\n"
            rt.append(res)
        return "\n\\vspace{12pt}\n\n".join(rt)
    def get_skills(skills):
        res = r"\begin{tabular}{ @{} >{\bfseries}l @{\hspace{6ex}} l }" + "\n"
        for k, v in skills:
            res += r"<key> & <val> \\".replace("<key>", k).replace("<val>", v) + "\n"
        return res + "\n" + r"\end{tabular}"
    def mockData():
        experience = [[('March 2012', 'Present'),
              ('Layer BV', 'Amsterdam, The Netherlands'),
              'J2EE Analyst programmer',
              'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec et auctor neque. Nullam ultricies sem sit amet magna tristique imperdiet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Phasellus eget mollis nunc',
              {'Languages': 'J2EE'}],
             [('March 2009', 'August 2010 (Part Time)'),
              ('Buy More', 'New York, USA'),
              'Supermarket Clerk',
              'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec et auctor neque. Nullam ultricies sem sit amet magna tristique imperdiet',
              {}]]
        education = [
            [("January 2011", "February 2012"), "Master of Science in Computer Science",
             "First Class Honours", ("The University of California", "Los Angeles, USA"),
             "more information goes here"
            ], 
            [("August 2008", "September 2010"), "Bachelor of Science in Computer Science", "With Distinction",("New York University", "New York, USA"),
             "ipsum dolor sit amet, consectetur adipiscing elit. Donec et auctor neque. Nullam ultricies"
            ]
        ]
        skills = [
            ("Computer Languages", "Prolog, Haskell, AWK, Erlang, Scheme, ML"),
            (r"Protocols \& APIs", "XML, JSON, SOAP, REST"),
            ("Databases", "MySQL, PostgreSQL, Microsoft SQL" ),
            ("Tools", "SVN, Vim, Emacs")
        ]
        return ObjMaker.variablesAndFunction(locals())
    def get_content(obje, exp, education, skills, fullName, streetName, city, zip, country, email, phone):
        content = DicOps.get(SerializationDB.readPickle(LibsDB.picklePath("temps")), ['timeline', '2025', '01_Jan', 'cv-template1'])
        tt = {'<streetname>': ('44', streetName),
         '<city>': ('44', city),
         '<zip>': ('44', zip),
         '<country>': ('44', country),
         '<email>': ('45', email),
         '<phone>': ('45', phone),
         '<11FullName11>': ('58', fullName),
         '<11ObjectiveContent11>': ( '68', obje),
         '<11WorkExperience11>': ('76', s.handlers.getWorkExperience(exp)),
         '<11Education11>': ('84', s.handlers.get_education(education)),
         '<11Skills11>': ('92', s.handlers.get_skills(skills))}
        for k in tt:
            nr, v = tt[k]
            content[nr] = content[nr].replace(k, v)
        return "\n".join(list(map(lambda x:content[x],sorted(content, key=lambda x: int(x)))))
    s = ObjMaker.variablesAndFunction(locals())
    return s
def CVTemplate1():
    tm = TemplateModel1()
    person_dataWid = Utils.get_comp({"options": tm.handlers.get_options_for_personal_infos()}, IpywidgetsComponentsEnum.Dropdown, className = "w-auto")
    def generate():
        pass
    
    s = ObjMaker.uisOrganize(locals())
    return s
def TemplateModel1():
    data = SerializationDB.readPickle(os.sep.join([LibsDB.cloudPath(), 'timeline', '2024', '12_Dec', 'jobSearchData.pkl']))
    temp = {}
    
    def get_options_for_personal_infos():
        infos = s.handlers.get_layer2("infos")
        pi = infos["personal infos"]["infos"]["data"]
        return list(map(lambda x: pi[x]["first name"], pi))
    def get_layer2(name):
        if name in s.process.temp:
            return s.process.temp[name]
        s.process.temp[name] = s.handlers.getAsDic(s.process.layer1[name]["more info"], "name", ["infos"])
        return s.process.temp[name]
    def get_personal_info_for(firstName):
        infos = s.handlers.get_layer2("infos")
        pi = infos["personal infos"]["infos"]["data"]
        ky = list(filter(lambda x: pi[x]["first name"] == firstName, pi))
        if len(ky):
            da =  pi[ky[-1]]
            fn = da["first name"] +  " " + da["last name"]
            addr = da["street"] + " " +  da["house nr"]
            return fn,da["email"],da["phone"], addr, da["city"], da["zip"], da["country"]
    def get_objective():
        k = "Programming, Information processing"
        dt = s.process.infos["looking for"]["infos"]
        infs = s.handlers.getAsList(dt, "title", ["description"])
        return infs[k][0]
    def getAsList(data, keyIndex , dataKeys):
        res = {}
        for k, v in data["data"].items():
            res[v[keyIndex]] = [v[kk] for kk in dataKeys]
        return res
    def get_education():
        ly2 = s.process.infos
        eduInfo = s.handlers.getAsList(ly2["Education"]["infos"], "degree title", ["note", "description", "institution", "content infos"])
        inst = s.handlers.getAsList(ly2["Institution"]["infos"], "name", ["location","country", "from", "till"])
        # now.strftime()
        format = "%d.%m.%Y"
        res = []
        for ti in eduInfo:
            nt, des, ins, ci = eduInfo[ti]
            loc,ct,fr,till = inst[ins]
            res.append([(fr.strftime(format), till), ti, nt, (ins, loc + ", " + ct), des])
        return res
    def get_work_exp():
        ly2 =s.process.infos
        pp = s.handlers.getAsList(ly2["Personal Project"]["infos"], "title", ["description", "preview infos"])
        we = s.handlers.getAsList(ly2["Work Experience"]["infos"], "title", ["institution","description", "from", "till", "preview infos"])
        ins = s.handlers.getAsList(ly2["Institution"]["infos"], "name", ["location","country", "from", "till"])
        res = []
        for ti in we:
            i,des,f,t,pi = we[ti]
            lc, co, fi,_ = ins[i]
            format = "%B %Y"
            d = []
            d.append((f.strftime(format), t.strftime(format)))
            d.append((i, lc + ", "+  co))
            d.append(ti)
            d.append(des)
            d.append({})
            res.append(d)
        return res
    def get_skills():
        ly2 = s.process.infos
        infos = s.handlers.getAsList(ly2["Skill"]["infos"], "title", ["category"])
        cg = {}
        for l in infos:
            g = infos[l][0]
            if g not in cg:
                cg[g] = []
            cg[g].append(l)
        return [(k, ",".join(cg[k])) for k in cg]
    def getAsDic(data, keyIndex , dataKeys):
        res = {}
        for k, v in data["data"].items():
            res[v[keyIndex]] = {kk: v[kk] for kk in dataKeys}
        return res
    layer1 = getAsDic(data, "title", ["more info"])
    s = ObjMaker.variablesAndFunction(locals())
    s.process.infos = get_layer2("infos")
    return s
class Main:
    def make_template1():
        te = Template1()
        tm = TemplateModel1()
        fn, em, ph, add, city, zip, cou = tm.handlers.get_personal_info_for("Raja Babu")
        cc = te.handlers.get_content(
            tm.handlers.get_objective(), tm.handlers.get_work_exp(), tm.handlers.get_education(),  tm.handlers.get_skills(),
            fn, add, city, zip, cou, em, ph
        )
        makePdf(cc)