import WordDatabase

import ProductDatabase
from GCSODatabase import GCSODatabase

class Token:

    def __init__(self, intent, topic, action, query):
        self.intent = intent
        self.topic = topic
        self.action = action
        self.query = query

    def process(self):
        WB = WordDatabase.WordDatabase()
        PLD = ProductDatabase.ProductLanguageDatabase()
        GCSO = GCSODatabase()
        modiflag = False
        for act in self.action:
            if (act.lower() == "localize" or act.lower() == "localise" or act.lower() == "translate") and len(self.query) == 0:
                for top in self.topic:
                    if top in WB.dataProduct:
                        self.project.setProduct(top)
                        modiflag = True
                    elif top in WB.dataLanguage:
                        self.project.addLanguage(top)
                        modiflag = True
        print modiflag
        if modiflag == True:
            if(self.project.checkComplete()) == False:
                list = self.project.getIncompleteField()
                return "What about " + list[0] + "?"
            else:
                return "The total output should be 2000 dollars"
                self.project.clear()
        else:
            for intent in self.intent:
                for top in self.topic:
                    for action in self.action:
                        if action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and (
                            PLD.getMatchScore(top.strip()) > 3500):
                            if len(set([s.strip().lower() for s in self.topic]).intersection(set(WB.dataLastVersion))) == 0:
                                lang = False
                                lang_option = None
                                for q in top.strip().split(" "):
                                    if q.lower() in [l.lower() for l in PLD.getAllLangOptions()]:
                                        lang = True
                                        lang_option = q
                                if lang == True:
                                    pdt_name = top.strip().replace(lang_option, '')
                                    product = PLD.findClosetMatch(pdt_name)
                                    ans = "The product " + product + " in language " + lang_option + " is releasing in "
                                    ptok = GCSO.findProductLanguage(product, lang_option)
                                else:
                                    pdt_name = top.strip()
                                    print pdt_name
                                    product = PLD.findClosetMatch(pdt_name)
                                    print product
                                    ans = "The product " + product + " was released in "
                                    ptok = GCSO.findProduct(product)
                                try:
                                    assert ptok != None
                                except AssertionError:
                                    return "Internal Database Error"
                                ans = ans + ptok.FCSDate
                            else:
                                pdt_name = top.strip()
                                print pdt_name
                                product = PLD.findClosetMatch(pdt_name)
                                print product
                                ans = "The most recent version of product " + product + " was released in "
                                ptok = GCSO.findProduct(product, last=True)
                                try:
                                    assert ptok != None
                                except AssertionError:
                                    return "Internal Database Error"
                                ans = ans + ptok.FCSDate
                            return ans



            for query in self.query:
                for intent in self.intent:
                    for top in self.topic:
                        for action in self.action:

                            if query.lower().strip() in WB.dataQuriesLang and (PLD.getMatchScore(top.strip()) > 3500) and intent.lower().strip() in WB.dataQuestionHowMuch:
                                #Return avaliable languages for the product.
                                languages = PLD.getAllAvaliableLanguages(PLD.findClosetMatch(top.strip()))
                                ans_str = "The product " + PLD.findClosetMatch(top.strip()) + " is available in "
                                for i in range(0, len(languages) -1):
                                    ans_str = ans_str + languages[i] + ", "
                                ans_str = ans_str + "and " + languages[-1] + "."
                                return ans_str
                            elif (query.lower().strip() in WB.dataQueryTypeTime) and (PLD.getMatchScore(top.strip()) > 3500) and (intent.lower().strip() in WB.dataQuestionWhat):
                                lang = False
                                lang_option = None
                                for q in top.strip().split(" "):
                                    if q.lower() in [l.lower() for l in PLD.getAllLangOptions()]:
                                        lang = True
                                        lang_option = q
                                if lang == True:
                                    pdt_name = top.strip().replace(lang_option, '')
                                    print pdt_name
                                    product = PLD.findClosetMatch(pdt_name)
                                    ans = "The product " + product + " in language " + lang_option + " is releasing in "
                                    ptok = GCSO.findProductLanguage(product, lang_option)
                                else:
                                    pdt_name = top.strip()
                                    product = PLD.findClosetMatch(pdt_name)
                                    print product
                                    ans = "The product " + product + " is releasing in "
                                    ptok = GCSO.findProduct(product)
                                try:
                                    assert ptok != None
                                except AssertionError:
                                    return "Internal Database Error"
                                ans = ans + ptok.FCSDate
                                return ans
                            elif action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and (PLD.getMatchScore(query.strip()) > 3500) :
                                lang = False
                                lang_option = None
                                for q in query.strip().split(" "):
                                    if q.lower() in [l.lower() for l in PLD.getAllLangOptions()]:
                                        lang = True
                                        lang_option = q
                                if lang == True:
                                    pdt_name = top.strip().replace(lang_option, '')
                                else:
                                    pdt_name = top.strip()
                                product = PLD.findClosetMatch(pdt_name)
                                ans = "The product " + product + " is releasing in "
                                ptok = GCSO.findProduct(product)
                                try:
                                    assert ptok != None
                                except AssertionError:
                                    return "Internal Database Error"
                                ans = ans + ptok.FCSDate
                                return ans
                            elif query.lower().strip() == "development processes" and top in WB.dataProduct:
                                return "The product " + top + " needs Kit Prep, SW Engineering processes in localization. "
                            elif query.lower().strip() == "li units" and (PLD.getMatchScore(query.strip()) > 3500) :
                                for field in self.topic:
                                    if field.strip() in WB.dataDevComponents:
                                        return "The " + field + " process of product " + top + " needs 10 LI Units to finish. "
                            elif (PLD.getMatchScore(query.strip()) > 3500):
                                for intent in self.intent:
                                    if intent.lower().strip() == "available":
                                        for sub in self.topic:
                                            if sub.strip() in PLD.getAllLangOptions():
                                                if PLD.checkLanguageAvaliability(PLD.findClosetMatch(query),
                                                                                 sub.strip()):
                                                    return "The product " + PLD.findClosetMatch(query) + " is available in " + sub + "."
                                                else:
                                                    return "The product " + PLD.findClosetMatch(query) + " is not available in " + sub + "."
            for intent in self.intent:
                for query in self.query:
                    for top in self.topic:

                        if query.lower().strip() in WB.dataQuriesLang and (PLD.getMatchScore(top.strip()) > 3500) and intent.lower().strip() in WB.dataQuestionHowMuch:
                            #Return avaliable languages for the product.
                            languages = PLD.getAllAvaliableLanguages(PLD.findClosetMatch(top.strip()))
                            ans_str = "The product " + PLD.findClosetMatch(top.strip()) + " is available in "
                            for i in range(0, len(languages) -1):
                                ans_str = ans_str + languages[i] + ", "
                            ans_str = ans_str + "and " + languages[-1] + "."
                            return ans_str
                        elif query.lower().strip() in WB.dataQuriesLang and (PLD.getMatchScore(top.strip()) > 3500) and intent.lower().strip() in WB.dataQuestionWhat:
                            languages = PLD.getAllAvaliableLanguages(PLD.findClosetMatch(top.strip()))
                            ans_str = "The product " + PLD.findClosetMatch(top.strip()) + " is available in "
                            for i in range(0, len(languages) - 1):
                                ans_str = ans_str + languages[i] + ", "
                            ans_str = ans_str + "and " + languages[-1] + "."
                            return ans_str
                        elif (intent.strip().lower() in WB.dataQuestionWhat) and (
                            query.strip().lower() in WB.dataLangGap):
                            entities = top.split("and")
                            pdt1 = PLD.findClosetMatch(entities[0].strip())
                            pdt2 = PLD.findClosetMatch(entities[1].strip())
                            gap1, gap2 = PLD.getLanguageGap(pdt1, pdt2)
                            ans = ""

                            if len(gap1) == 0 and len(gap2) == 0:
                                return "The second product " + pdt2 + " is compatitable with all the language supported by the first product " + pdt1 + "."

                            if len(gap1) != 0:
                                ans = "The first product " + pdt1 + " has "
                                for i in range(0, len(gap1) - 1):
                                    ans = ans + gap1[i] + ", "
                                ans = ans + " and " + gap1[-1] + " while the second product " + pdt2 + " has not. "
                            else:
                                ans = ans + "The second product " + pdt2 + " is compatitable with all the language supported by the first product " + pdt1 + "."

                            if len(gap2) != 0:
                                ans = ans + "The second product " + pdt2 + " has "
                                for i in range(0, len(gap2) - 1):
                                    ans = ans + gap2[i] + ", "
                                ans = ans + " and " + gap2[-1] + " while the first product " + pdt1 + " has not. "
                            else:
                                ans = ans + "The first product " + pdt1 + " is compatitable with all the language supported by the second product " + pdt2 + "."

                            return ans
                        elif query.lower().strip() == "development processes" and (PLD.getMatchScore(top.strip()) > 3500) :
                            return "The product " + top + " needs Kit Prep, SW Engineering processes in localization. "
                        elif query.lower().strip() == "li units" and (PLD.getMatchScore(top.strip()) > 3500) :
                            for field in self.topic:
                                if field.strip() in WB.dataDevComponents:
                                    return "The " + field + " process of product " + top + " needs 10 LI Units to finish. "
                        elif(PLD.getMatchScore(query.strip()) > 3500):
                            for intent in self.intent:
                                if intent.lower().strip() == "available":
                                    for sub in self.topic:
                                        if sub.strip() in PLD.getAllLangOptions():
                                            if PLD.checkLanguageAvaliability(PLD.findClosetMatch(query), sub.strip()):
                                                return "The product " + PLD.findClosetMatch(query) + " is available in " + sub + "."
                                            else:
                                                return "The product " + PLD.findClosetMatch(query) + " is not available in " + sub + "."


            for intent in self.intent:
                for query in self.query:
                    for action in self.action:
                        if action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and (PLD.getMatchScore(query.strip()) > 3500):
                            lang = False
                            lang_option = None
                            for q in query.strip().split(" "):
                                if q.lower() in [l.lower() for l in PLD.getAllLangOptions()]:
                                    lang = True
                                    lang_option = q
                            print lang_option
                            if lang == True:
                                pdt_name = query.strip().replace(lang_option, '')
                                print pdt_name
                                product = PLD.findClosetMatch(pdt_name)
                                ans = "The product " + product + " in language " + lang_option + " is releasing in "
                                ptok = GCSO.findProductLanguage(product, lang_option)
                            else:
                                pdt_name = query.strip()
                                product = PLD.findClosetMatch(pdt_name)
                                print product
                                ans = "The product " + product + " was released in "
                                ptok = GCSO.findProduct(product)
                            try:
                                assert ptok != None
                            except AssertionError:
                                return "Internal Database Error"
                            ans = ans + ptok.FCSDate
                            return ans

                        elif (PLD.getMatchScore(query.strip()) > 3500):
                            for intent in self.intent:
                                if intent.lower().strip() == "available":
                                    for sub in self.topic:
                                        if sub.strip() in PLD.getAllLangOptions():
                                            if PLD.checkLanguageAvaliability(PLD.findClosetMatch(query), sub.strip()):
                                                return "The product " + PLD.findClosetMatch(query) + " is available in " + sub + "."
                                            else:
                                                return "The product " + PLD.findClosetMatch(query) + " is not available in " + sub + "."


        return "I don't know"







