import WordDatabase

class Token:

    def __init__(self, intent, topic, action, query):
        self.intent = intent
        self.topic = topic
        self.action = action
        self.query = query


    def process(self):
        WB = WordDatabase.WordDatabase()
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
            for top in self.topic:
                for query in self.query:
                    if query.lower().strip() == "languages" and (top in WB.dataProduct):
                        #Return avaliable languages for the product.
                        return "The product " + top + " is available in English, Chinese and Japanese"
                    elif query.lower().strip() == "development processes" and top in WB.dataProduct:
                        return "The product " + top + " needs Kit Prep, SW Engineering processes in localization. "
                    elif query.lower().strip() == "li units" and top in WB.dataProduct:
                        for field in self.topic:
                            if field.strip() in WB.dataDevComponents:
                                return "The " + field + " process of product " + top + " needs 10 LI Units to finish. "

                    elif query.strip() in WB.dataProduct:
                        for intent in self.intent:
                            if intent.lower().strip() == "available":
                                for sub in self.topic:
                                    if sub.strip() in WB.dataLanguage:
                                        return "The product " + query + " is available in " + sub + "."

        return "I don't know"







