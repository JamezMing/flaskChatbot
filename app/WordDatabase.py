class WordDatabase:
    def __init__(self):
        self.dataGreetings = ["Hi, Congroo", "Hi Congroo", "Congroo", "Hi there"]
        self.dataKeyPhrases = ["LI Units", "word units", "words"]
        self.dataTime = ["time"]
        self.dataQuriesLang = ["languages", "versions", "language", "version", "locales", "locale"]
        self.dataAvaliability = ["are avaliable", "is avaliable", "was avaliable", "were avaliable"]
        self.dataLastVersion = ["last version", "previous version", "previous release", "last release", "recent release"]
        self.dataDevComponents = ["SW Engineering", "Testing Execution", "Testing Kit Prep"]
        self.dataPersonale = ["PM", "PM head", "GT head", "GT", "QM Automation", "PT", "PT head"]
        self.negation = ["not", "n't", "neither"]
        self.dataDevelopProcess = ["automated testing", "rebuild", "don't need any", "no process"]
        self.dataSpeed = ["quick", "quickly", "fast", "quickly", "take your time", "slow", "slowly"]
        self.dataProduct = ["FormIt Web", "FormIt iOS", "Autocad Construction", "Fusion 360", "Autocad 360", "BIM", "Sketches Pro", "Autocad"]
        self.dataQuestionHowMuch = ["how much","how many"]
        self.dataQuestionWho = ["who"]
        self.dataQuestionWhat = ["what"]
        self.dataQuestionTime = ["when", "what time"]
        self.dataQueryTypeTime = ["launch date", "release date", "publish date", "avaliable date", "announce date"]
        self.dataReleasing = ["releasing", "release", "released", "publish", "post", "upload", "launch", "available", "launched",  "announce", "disclose", "reveal", "distribute" , "translate", "translated"]
        self.dataAction = ["localise", "translate", "localize"]
        self.dataReset = ["new conversation", "start over", "end the session", "end session"]
        self.dataLangGap = ["language gap", "gap", "gap of language"]
    def isProduct(self, name):
        res = list()
        for pdt in self.dataProduct:
            for tok in pdt.lower().split(" "):
                if tok == name.strip().lower():
                    res.append(pdt)
            if pdt.lower() == name.strip().lower():
                res.append(pdt)
        return res