import WordDatabase
import pandas
import MySQLdb
import ProductDatabase

class Token:

    def __init__(self, intent, topic, action, query):
        self.intent = intent
        self.topic = topic
        self.action = action
        self.query = query

    def process(self):
        WB = WordDatabase.WordDatabase()
        PLD = ProductDatabase.ProductLanguageDatabase()
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

            for query in self.query:
                for intent in self.intent:
                    for top in self.topic:
                        for action in self.action:
                            print "Query: " + query
                            print "Topic: " + top
                            print "Intent: " + str(self.intent)

                            if query.lower().strip() in WB.dataQuriesLang and (PLD.isProduct(top.strip())) and intent.lower().strip() in WB.dataQuestionHowMuch:
                                #Return avaliable languages for the product.
                                languages = PLD.getAllAvaliableLanguages(top.strip())
                                ans_str = "The product " + top.strip() + " is available in "
                                for i in range(0, len(languages) -1):
                                    ans_str = ans_str + languages[i] + ", "
                                ans_str = ans_str + "and " + languages[-1] + "."
                                return ans_str
                            elif action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and (PLD.isProduct(top.strip())) :
                                return "The product " + top + " will be releasing in Jan 2017. "
                            elif query.lower().strip() == "development processes" and top in WB.dataProduct:
                                return "The product " + top + " needs Kit Prep, SW Engineering processes in localization. "
                            elif query.lower().strip() == "li units" and (PLD.isProduct(top.strip())) :
                                for field in self.topic:
                                    if field.strip() in WB.dataDevComponents:
                                        return "The " + field + " process of product " + top + " needs 10 LI Units to finish. "
                            elif query.strip() in WB.dataProduct:
                                for intent in self.intent:
                                    if intent.lower().strip() == "available":
                                        for sub in self.topic:
                                            if sub.strip() in WB.dataLanguage:
                                                return "The product " + query + " is available in " + sub + "."
            for intent in self.intent:
                for query in self.query:
                    for top in self.topic:
                            print "Query: " + query
                            print "Topic: " + top
                            print "Intent: " + str(self.intent)

                            if query.lower().strip() in WB.dataQuriesLang and (PLD.isProduct(top.strip()))  and intent.lower().strip() in WB.dataQuestionHowMuch:
                                #Return avaliable languages for the product.
                                languages = PLD.getAllAvaliableLanguages(top.strip())
                                ans_str = "The product " + top.strip() + " is available in "
                                for i in range(0, len(languages) -1):
                                    ans_str = ans_str + languages[i] + ", "
                                ans_str = ans_str + "and " + languages[-1] + "."
                                return ans_str
                            elif query.lower().strip() == "development processes" and (PLD.isProduct(top.strip())) :
                                return "The product " + top + " needs Kit Prep, SW Engineering processes in localization. "
                            elif query.lower().strip() == "li units" and (PLD.isProduct(top.strip())) :
                                for field in self.topic:
                                    if field.strip() in WB.dataDevComponents:
                                        return "The " + field + " process of product " + top + " needs 10 LI Units to finish. "
                            elif query.strip() in WB.dataProduct:
                                for intent in self.intent:
                                    if intent.lower().strip() == "available":
                                        for sub in self.topic:
                                            if sub.strip() in WB.dataLanguage:
                                                return "The product " + query + " is available in " + sub + "."

            for intent in self.intent:
                for query in self.query:
                    for action in self.action:

                            print "Query: " + query
                            print "Intent: " + str(self.intent)


                            if action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and (PLD.isProduct(query.strip())) :
                                return "The product " + query + " will be releasing in Jan 2017. "

                            elif (PLD.isProduct(query.strip())):
                                for intent in self.intent:
                                    if intent.lower().strip() == "available":
                                        for sub in self.topic:
                                            if sub.strip() in WB.dataLanguage:
                                                return "The product " + query + " is available in " + sub + "."

        return "I don't know"







