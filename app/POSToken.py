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
        for intent in self.intent:
            for top in self.topic:
                for action in self.action:
                    print "Route 1"
                    if action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and (len(PLD.getSimilarNames(top.lower().strip())) > 0):
                        if len(set([s.strip().lower() for s in self.topic]).intersection(set(WB.dataLastVersion))) == 0:
                            print "1-1"
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
                            print "1-2"
                            pdt_name = top.strip()
                            print pdt_name
                            product = PLD.findClosetMatch(pdt_name)
                            print product
                            ans = "The most recent version of product " + product + " was released in "
                            ptok = GCSO.findProduct(product)
                            try:
                                assert ptok != None
                            except AssertionError:
                                return "Internal Database Error"
                            ans = ans + ptok.FCSDate
                        return ans
                    if action.lower().strip() in WB.dataReleasing and len(PLD.getSimilarNames(top.lower().strip())) > 0 and (len(set(self.topic).intersection(set(PLD.getAllLangOptions())))!= 0) and len(self.query) == 0:
                        lang = list(set(self.topic).intersection(set(PLD.getAllLangOptions())))[0]
                        if PLD.checkLanguageAvaliability(PLD.findClosetMatch(top),
                                                         lang.strip()):
                            return "The product " + PLD.findClosetMatch(top) + " is available in " + lang + "."
                        else:
                            return "The product " + PLD.findClosetMatch(top) + " is not available in " + lang + "."
                    if "release date" in [s.strip().lower() for s in self.topic] and (len(PLD.getSimilarNames(top.lower().strip())) > 0) and (intent.lower().strip() in WB.dataQuestionTime):
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
                        return ans


        for query in self.query:
            for intent in self.intent:
                for top in self.topic:
                    for action in self.action:

                        if query.lower().strip() in WB.dataQuriesLang and (len(PLD.getSimilarNames(top.lower().strip())) > 0) and intent.lower().strip() in WB.dataQuestionHowMuch:
                            #Return avaliable languages for the product.
                            languages = PLD.getAllAvaliableLanguages(PLD.findClosetMatch(top.strip()))
                            ans_str = "The product " + PLD.findClosetMatch(top.strip()) + " is available in "
                            for i in range(0, len(languages) -1):
                                ans_str = ans_str + languages[i] + ", "
                            ans_str = ans_str + "and " + languages[-1] + "."
                            return ans_str
                        elif (query.lower().strip() in WB.dataQueryTypeTime) and (len(PLD.getSimilarNames(top.lower().strip())) > 0) and (intent.lower().strip() in WB.dataQuestionWhat):
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

                        elif query.lower().strip() in WB.dataQuriesLang and (len(PLD.getSimilarNames(top.lower().strip())) > 0) and (intent.lower().strip() in WB.dataQuestionWhat) and action.lower().strip() in WB.dataReleasing:
                            if len(set([s.strip().lower() for s in self.topic]).intersection(set(WB.dataLastVersion))) != 0:
                                pdt_name = top.strip()
                                print pdt_name
                                product = PLD.findClosetMatch(pdt_name)
                                print product
                                ans = "The most recent version of product " + product + " was released in "
                                langs = PLD.getAllAvaliableLanguages(product)

                                for l in langs[:-1]:
                                    ans = ans + l + ", "
                                ans = ans + " and " + langs[-1]
                                '''ptok = GCSO.findProduct(product, last=True)
                                language =  ""
                                langCode = ptok.langCodeName.split(", ")
                                langList = str(ptok.languageAvaliable).split(";#")
                                if langCode[0] == "Non-Language Specific":
                                    ans = "The most recently released version of product " + product + " has no language specified."

                                elif langCode[0] == "Regional Non-Specific EMEA" or langCode[
                                    0] == 'Rgnl Non-Specific AMER/E_EMEA' or langCode[
                                    0] == 'Regional Non-Specific APAC':
                                    for l in langList[:-1]:
                                        language = language + l + " "
                                    language = language + " and " + langList[-1]
                                else:
                                    for l in langCode[:-1]:
                                        language = language + l + " "
                                    language = language + " and " + langList[-1]'''
                                return ans



                        elif action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and ((len(PLD.getSimilarNames(query.strip())) > 0) ) :
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
                        elif query.lower().strip() == "li units" and ((len(PLD.getSimilarNames(query.strip())) > 0) ) :
                            for field in self.topic:
                                if field.strip() in WB.dataDevComponents:
                                    return "The " + field + " process of product " + top + " needs 10 LI Units to finish. "
                        elif ((len(PLD.getSimilarNames(query.strip())) > 0) ):
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

                    if query.lower().strip() in WB.dataQuriesLang and (len(PLD.getSimilarNames(top.lower().strip())) > 0) and intent.lower().strip() in WB.dataQuestionHowMuch:
                        #Return avaliable languages for the product.
                        languages = PLD.getAllAvaliableLanguages(PLD.findClosetMatch(top.strip()))
                        ans_str = "The product " + PLD.findClosetMatch(top.strip()) + " is available in "
                        for i in range(0, len(languages) -1):
                            ans_str = ans_str + languages[i] + ", "
                        ans_str = ans_str + "and " + languages[-1] + "."
                        return ans_str
                    elif query.lower().strip() in WB.dataQuriesLang and (len(PLD.getSimilarNames(top.lower().strip())) > 0) and intent.lower().strip() in WB.dataQuestionWhat:
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
                    elif query.lower().strip() == "development processes" and (len(PLD.getSimilarNames(top.lower().strip())) > 0) :
                        return "The product " + top + " needs Kit Prep, SW Engineering processes in localization. "
                    elif query.lower().strip() == "li units" and (len(PLD.getSimilarNames(top.lower().strip())) > 0) :
                        for field in self.topic:
                            if field.strip() in WB.dataDevComponents:
                                return "The " + field + " process of product " + top + " needs 10 LI Units to finish. "
                    elif((len(PLD.getSimilarNames(query.strip())) > 0) ):
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
                    if action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and (len(PLD.getSimilarNames(query.strip())) > 0) :
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

                    elif ((len(PLD.getSimilarNames(query.strip())) > 0)):
                        for intent in self.intent:
                            if intent.lower().strip() == "available":
                                for sub in self.topic:
                                    if sub.strip() in PLD.getAllLangOptions():
                                        if PLD.checkLanguageAvaliability(PLD.findClosetMatch(query), sub.strip()):
                                            return "The product " + PLD.findClosetMatch(query) + " is available in " + sub + "."
                                        else:
                                            return "The product " + PLD.findClosetMatch(query) + " is not available in " + sub + "."


        return "I don't know"







