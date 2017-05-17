import WordDatabase
import pandas
import MySQLdb


class Token:

    def __init__(self, intent, topic, action, query):
        self.intent = intent
        self.topic = topic
        self.action = action
        self.query = query
        dbfile = open('/home/james/PycharmProjects/flaskChatbot/database/db.csv')
        import csv, sqlite3

        con = sqlite3.connect(":memory:")
        con.text_factory = str

        cur = con.cursor()
        cur.execute("CREATE TABLE t (Language, French, Italian, German, Spanish, Japanese, Korean, Simplified_Chinese, Tranditional_Chinese, Czech, "
                        "Hungarian, Russian, Polish, Brazilian_Portuguese, Danish, Finnish, Dutch, Norwegian"
                        ",Swedish,  Romanian, Portuguese, Arabic, Hindi, Indonesian, Thai, Turkish, "
                        "Vietnamese, Hebrew);")  # use your column names here

        with open('/home/james/PycharmProjects/flaskChatbot/database/db.csv', 'rb') as fin:  # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['Count of Language'], i['French'], i['Italian'], i['German'], i['Spanish'], i['Japanese'], i['Korean'], i['Simplified Chinese'],
                      i['Tranditional Chinese'], i['Czech'], i['Hungarian'], i['Russian'], i['Polish'], i['Brazilian Portuguese'], i['Danish'],
                      i['Finnish'], i['Dutch'], i['Norwegian'], i['Swedish'], i['Romanian'], i['Portuguese'], i['Arabic'],
                      i['Hindi'], i['Indonesian'], i['Thai'], i['Turkish'], i['Vietnamese'], i['Hebrew']) for i in dr]

            print len(to_db[0])
        cur.executemany("INSERT INTO t (Language, French, Italian, German, Spanish, Japanese, Korean, Simplified_Chinese, Tranditional_Chinese, Czech, "
                        "Hungarian, Russian, Polish, Brazilian_Portuguese, Danish, Finnish, Dutch, Norwegian"
                        ",Swedish,  Romanian, Portuguese, Arabic, Hindi, Indonesian, Thai, Turkish, "
                        "Vietnamese, Hebrew) VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
        con.commit()
        #con.close()
        self.df = con
        cur.execute("SELECT * FROM t")
        print cur.fetchall()



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

            for query in self.query:
                for intent in self.intent:
                    for top in self.topic:
                        for action in self.action:
                            print "Query: " + query
                            print "Topic: " + top
                            print "Intent: " + str(self.intent)

                            if query.lower().strip() in WB.dataQuriesLang and (top.strip() in WB.dataProduct) and intent.lower().strip() in WB.dataQuestionHowMuch:
                                #Return avaliable languages for the product.
                                return "The product " + top + " is available in English, Chinese and Japanese"
                            elif action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and (top.strip() in WB.dataProduct):
                                return "The product " + top + " will be releasing in Jan 2017. "
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
            for intent in self.intent:
                for query in self.query:
                    for top in self.topic:
                            print "Query: " + query
                            print "Topic: " + top
                            print "Intent: " + str(self.intent)

                            if query.lower().strip() in WB.dataQuriesLang and (top.strip() in WB.dataProduct) and intent.lower().strip() in WB.dataQuestionHowMuch:
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

            for intent in self.intent:
                for query in self.query:
                    for action in self.action:

                            print "Query: " + query
                            print "Intent: " + str(self.intent)


                            if action.lower().strip() in WB.dataReleasing and intent.lower().strip() in WB.dataQuestionTime and (query.strip() in WB.dataProduct):
                                return "The product " + query + " will be releasing in Jan 2017. "

                            elif query.strip() in WB.dataProduct:
                                for intent in self.intent:
                                    if intent.lower().strip() == "available":
                                        for sub in self.topic:
                                            if sub.strip() in WB.dataLanguage:
                                                return "The product " + query + " is available in " + sub + "."

        return "I don't know"







