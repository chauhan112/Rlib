import os

class TimelineDB:
    def getMonthPath(monthNr):
        from TimeDB import TimeDB
        months = ['1. jan',
             '2. feb',
             '3. mar',
             '4. apr',
             '5. may',
             '6. jun',
             '7. jul',
             '8. aug',
             '9. sep',
             '10. oct',
             '11. nov',
             '12. dec']
        m = ''
        if(type(monthNr) == int):
            m = months[monthNr]
        elif(type(monthNr)==str):
            fil = list(filter(lambda x: monthNr.lower() in x, months))
            if(len(fil)== 1):
                m = fil[0]
            else:
                raise IOError("not unique letters combination")
        else:
            raise IOError("Invalid type. Only str or int is allowed 0 for jan")
        year = TimeDB.today()[0][0]
        return os.sep.join([TimelineDB.getYearPath(year), m])

    def getYearPath(year):
        from LibsDB import LibsDB
        return os.sep.join([LibsDB.cloudPath().replace("\\", os.sep),'timeline', str(year)])
    