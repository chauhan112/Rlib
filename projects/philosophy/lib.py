
class ISubject:
    def get_identifier(self):
        pass
    def lies_in_subject(self, sub):
        pass
class Tools:
    _lemmatizer =None
    _nlp = None
    def baseform(word, *params):
        from nltk.stem.wordnet import WordNetLemmatizer
        if Tools._lemmatizer is None:
            Tools._lemmatizer = WordNetLemmatizer()
        return Tools._lemmatizer.lemmatize(word,*params).lower()
    def spacy_baseform(word):
        if Tools._nlp is None:
            Tools._initialize()
        nlp = Tools._nlp
        processed_text = nlp(word)
        for token in processed_text:
            return token.lemma_
    def _initialize():
        import spacy
        spacy.prefer_gpu()
        Tools._nlp = spacy.load("en_core_web_sm")

class NormalSubject:
    def __init__(self, sub: str):
        if type(sub) != str:
            sub = str(sub)
        self._subject = sub
        self._determinant = None
    def get_identifier(self):
        return self._subject
    def lies_in_subject(self, sub:ISubject):
        if self._determinant is None or self._determinant == "all":
            return self._compare(self._subject, sub.get_identifier())
        return False
    def set_deteminant(self, dete):
        self._determinant = dete
    def _compare(self, word1, word2):
        return Tools.spacy_baseform(word1) == Tools.spacy_baseform(word2)
class IStatement:
    def get_subject(self) -> ISubject:
        pass
    def get_object(self) -> ISubject:
        pass
    def get_action(self) -> ISubject:
        pass
class Premise(IStatement):
    def from_sentence(self, sentence: str):
        self._line = sentence
        import spacy
        spacy.prefer_gpu()
        nlp = spacy.load("en_core_web_sm")
        tokens = nlp(self._line)
        sub = NormalSubject(None)
        for token in tokens:
            if token.dep_ == "det":
                sub.set_deteminant(token)
            elif token.dep_ == "nsubj":
                sub._subject = token
            elif token.dep_ == "ROOT":
                self.set_action(NormalSubject(token))
            elif token.dep_ in ['dobj',"acomp", "attr","oprd"]:
                self.set_object(NormalSubject(token))
        self.set_subject(sub)
    def set_subject(self, sub: ISubject):
        self._sub = sub
    def set_object(self, obj: ISubject):
        self._obj = obj
    def set_action(self, action):
        self._action = action
    def get_subject(self) -> ISubject:
        return self._sub
    def get_object(self) -> ISubject:
        return self._obj
    def get_string(self):
        return self._line
    def get_action(self):
        return self._action
class IArgumentation:
    pass
class IValidity:
    def is_true(self, sen: IStatement):
        pass
class _PremisesSet:
    def set_premises(self, premises: list[IStatement]):
        self._premises = premises
class ManualValidityChecker(IValidity, _PremisesSet):
    def determine_truths(self):
        self._validity = {}
        for p in self._premises:
            disp_str = p.get_string()
            print(disp_str, end = "")
            tru = input("is this premise true? [y/n]: ")
            print()
            self._validity[disp_str] = (tru.strip().lower() not in ["", "false", "f", "wrong",'n'])
    def is_true(self, sen: Premise):
        return self._validity[sen.get_string()]
class AllTrue(IValidity):
    def is_true(self, x):
        return True
class IKeyMaker:
    def get_key(self, param):
        pass
class GKeyMaker:
    def __init__(self):
        self.set_key_func(lambda x: Tools.spacy_baseform(self._default_func(x)))
    def set_key_func(self, func):
        self._func  = func
    def get_key(self, tokenOrStr):
        return self._func(tokenOrStr)
    def _default_func(self, word):
        if type(word) == str:
            return word
        elif isinstance(word, NormalSubject):
            return str(word.get_identifier())
        return str(word)
class DeductiveArgumentation(IArgumentation, _PremisesSet):
    def __init__(self):
        mk = GKeyMaker()
        self.set_key_maker(mk)
    def check_conclusion(self, conclusion: IStatement):
        sub: NormalSubject = conclusion.get_subject()
        obj = conclusion.get_object()
        act = conclusion.get_action()
        maps = self._parse()
        try:
            while True:
                pact, ob, premise = maps[self._key_maker.get_key(sub)]
                if not self._validity_checker.is_true(premise):
                    return False
                if ob.lies_in_subject(obj):
                    return self._key_maker.get_key(pact._subject)  == self._key_maker.get_key(act._subject)
                sub = ob
        except Exception as e:
            print(e)
        return False

    def _parse(self):
        dic ={}
        for p in self._premises:
            sub = p.get_subject()
            obj = p.get_object()
            ac = p.get_action()
            key = self._key_maker.get_key(sub)
            if key not in dic:
                dic[key] = (ac, obj, p)

        return dic
    def set_validity_checker(self, checker: IValidity):
        self._validity_checker = checker
    def set_key_maker(self, key_maker: IKeyMaker):
        self._key_maker = key_maker
def premises_from_sentences(sentences: list[str]):
    res = []
    for sent in sentences:
        p = Premise()
        p.from_sentence(sent)
        res.append(p)
    return res
class Main:
    def verify(sentences:list[str], conclusion: str, verifier: IValidity = None):
        premises = premises_from_sentences(sentences)
        con = Premise()
        con.from_sentence(conclusion)
        if verifier is None:
            mvc = ManualValidityChecker()
            mvc.set_premises(premises)
            mvc.determine_truths()
            verifier = mvc
        da = DeductiveArgumentation()
        da.set_premises(premises)
        da.set_validity_checker(verifier)
        return da.check_conclusion(con)
class Example:
    def example1():
        sentences = [
            'Aik is a Bik.',
            'Bik is a Cik.',
            'Cik is a Milk.'
        ]
        conclusion_st = 'Aik is a Milk.'
        assert Main.verify(sentences, conclusion_st, AllTrue())
        assert Main.verify(sentences, "I am king.", AllTrue()) == False
    def example2():
        sentences = [
            'All humans are mortal.',
            'Socrates is a human.',
        ]
        conclusion_st = 'Socrates is mortal.'
        assert Main.verify(sentences, conclusion_st, AllTrue())
        assert Main.verify(sentences, "Socrates is immortal.", AllTrue()) == False