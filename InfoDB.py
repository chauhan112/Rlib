class InfoDB:
    def coronaInfo(moreCountry = []):
        import webbrowser
        countries = []
        from AIAlgoDB import AIAlgoDB
        countriesOfInterest = ['Nepal', "germany", "India", "brazil", "us"]
        k = AIAlgoDB.incrementalSearch(countriesOfInterest)
        if(type(moreCountry) == list):
            for c in moreCountry:
                countries += k.search(c)
        elif(type(moreCountry) == str):
            countries += k.search(moreCountry)
        for country in countries:
            webbrowser.open(f"https://www.worldometers.info/coronavirus/country/{country}/")
    
    def sayings():
        sayings = ['Skills speak louder than resumes',
        'nothing is more dangerous than playing it safe']
        from Database import Database
        return Database.getDB(sayings, displayer=print)

    def frequentGeneralInfos(word= None):
        from Database import Database
        dic = {
            'my floor printer work': 'Canon LBP6750/3560'
        }
        db = Database.dicDB(dic)
        return Database.dbSearch(db, word)

    def personalInfos(word = None):
        from Database import Database
        dic = {
            'phone number': '01627078024',
            'master card nr': '5401 8712 7678 0440',
            'master card expiry date': '11/2020',
            'gmail': 'ichbinsternchen43@gmail.com',
            'pythonanywhere': "TurboRaja"
        }
        db = Database.dicDB(dic)
        return Database.dbSearch(db, word)