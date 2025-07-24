import datetime
class MiscDB:
    def nepal_flag(height = '100'):
        from IPython.display import SVG
        from useful.WordDB import WordDB
        k = SVG(url='https://upload.wikimedia.org/wikipedia/commons/9/9b/Flag_of_Nepal.svg')
        return SVG(WordDB.replaceWithRegex("height=\"\d+\"", f"height=\"{height}\"", k.data))
    def compileFiles(files):
        from useful.OpsDB import OpsDB
        cmds = []
        for file in files:
            cmds.append(f"""g++ -Wall -g -c '{file}' -o '{file[:-4]+ ".o"}'""")
        for command in cmds:
            OpsDB.cmd(command)
        return list(map(lambda x: x[:-4]+ '.o', cmds))

    def compileAndLink(files):
        pass

    def get_country_confirmed_infected(country, start_date = None, end_date = None):
        from datetime import datetime, timedelta
        import requests
        if(end_date is None):
            end_date = datetime.now().date()
        if(start_date is None):
            start_date = end_date - timedelta(days=7)
        
        resp = requests.get(f"https://api.covid19api.com/country/{country}/status/confirmed",
                            params={"from": start_date,
                                    "to": end_date})
        return resp.json()

    def getMessage(country):
        from dateutil.parser import parse
        cases = MiscDB.get_country_confirmed_infected(country )
        latest_day = cases[-1]
        earliest_day = cases[0]
        percentage_increase = (latest_day['Cases'] - earliest_day['Cases']) / (earliest_day['Cases'] / 100)
        msg = f"There were {latest_day['Cases']} confirmed COVID cases in {country} " \
            f"on {parse(latest_day['Date']).date()}\n"

        msg += f"This is {round(abs(percentage_increase), 4)}% increase over the last week. " \
                    f"Travel is not recommended."
        return msg
        