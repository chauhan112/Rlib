class LanguageDB:
    def polite(word = None):
        from useful.Database import Database
        dic = {
            'why did u send me this link?': "I've taken a look at the link you sent me, but there must be something about it that I missed. What was it that you were particularly wanting to draw my attention to there?",
            'what do u mean by sth?':"I'm sorry, but I do not understand the word/phrase xxx. Would you please rephrase it for me?"
        }
        db = Database.dicDB(dic)
        return Database.dbSearch(db,word)