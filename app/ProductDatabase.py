import csv, sqlite3
from fuzzywuzzy import fuzz, process
import POSTagger

blacklist = ['for', 'in', 'with']
class ProductLanguageDatabase:
    def __init__(self, path = '/home/james/PycharmProjects/flaskChatbot/database/db.csv'):
        self.tagger = POSTagger.POSTagger()
        con = sqlite3.connect(":memory:", check_same_thread=False)
        con.text_factory = str

        cur = con.cursor()
        cur.execute(
            "CREATE TABLE t (Language, French, Italian, German, Spanish, Japanese, Korean, 'Simplified Chinese', 'Chinese' ,'Tranditional Chinese', Czech, "
            "Hungarian, Russian, Polish, 'Brazilian Portuguese', Danish, Finnish, Dutch, Norwegian"
            ",Swedish,  Romanian, Portuguese, Arabic, Hindi, Indonesian, Thai, Turkish, "
            "Vietnamese, Hebrew);")  # use your column names here

        with open(path,'rb') as fin:  # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['Count of Language'], i['French'], i['Italian'], i['German'], i['Spanish'], i['Japanese'],
                      i['Korean'], i['Simplified Chinese'],i['Simplified Chinese'],
                      i['Tranditional Chinese'], i['Czech'], i['Hungarian'], i['Russian'], i['Polish'],
                      i['Brazilian Portuguese'], i['Danish'],
                      i['Finnish'], i['Dutch'], i['Norwegian'], i['Swedish'], i['Romanian'], i['Portuguese'], i['Arabic'],
                      i['Hindi'], i['Indonesian'], i['Thai'], i['Turkish'], i['Vietnamese'], i['Hebrew']) for i in dr]

        cur.executemany(
            "INSERT INTO t (Language, French, Italian, German, Spanish, Japanese, Korean, 'Simplified Chinese', Chinese, 'Tranditional Chinese', Czech, "
            "Hungarian, Russian, Polish, 'Brazilian Portuguese', Danish, Finnish, Dutch, Norwegian"
            ",Swedish,  Romanian, Portuguese, Arabic, Hindi, Indonesian, Thai, Turkish, "
            "Vietnamese, Hebrew) VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            to_db)
        con.commit()
        #con.close()
        self.df = con
        query = "PRAGMA table_info(t);"
        cur = self.df.cursor()
        cur.execute(query)
        res = cur.fetchall()
        res_col = [i[1] for i in res]
        self.langdict = {}
        for i in range(0, len(res_col)):
            self.langdict[i] = res[i][1]

    def checkLanguageAvaliability(self, product, language):
        #Is Autocad 360 avaliable in French?, return boolean
        query = "SELECT " + language + " FROM t WHERE Language = '" + product + "'"
        cur = self.df.cursor()
        cur.execute(query)
        #print cur.fetchall()
        res = cur.fetchall()
        if res[0][0] == '':
            return False
        elif int(float(res[0][0])) != 0:
            return True

    def getAllUnavaliableProducts(self, language):
        #What are the products avaliable in French?
        query = "SELECT Language FROM t WHERE " + language + " IS NULL OR " + language + " = ''"
        cur = self.df.cursor()
        cur.execute(query)
        print cur.fetchall()

    def getAllAvaliableLanguages(self, product):
        query = "SELECT * FROM t WHERE UPPER(Language) = '" + product.upper() + "'"
        res = []
        cur = self.df.cursor()
        cur.execute(query)
        stats = cur.fetchall()[0]
        for i in range(1, len(stats)):
            if stats[i] != '':
                res.append(self.langdict.get(i))
        return res


    def isProduct(self, name):
        query = "SELECT Language FROM t WHERE UPPER(Language) = '" + name.upper() + "'"
        cur = self.df.cursor()
        cur.execute(query)
        res = cur.fetchall()
        if len(res) == 0:
            return False
        else:
            return True

    def findClosetMatch(self, name):
        query = "SELECT Language FROM t"
        cur = self.df.cursor()
        cur.execute(query)
        res = [r[0] for r in cur.fetchall()]
        max = 0
        match = ""
        poset = process.extract(name, res)
        for po in poset:
            score = int(fuzz.token_sort_ratio(name, po[0])) * int(po[1])
            if score > max:
                max = score
                match = po[0]
        return match


    def findPossibleMatches(self, name):
        query = "SELECT Language FROM t"
        cur = self.df.cursor()
        cur.execute(query)
        res = [r[0] for r in cur.fetchall()]
        return process.extract(name, res)

    def getMatchScore(self, name):
        name_arr = name.split(" ")
        for n in name_arr:
            if n.lower() in [l.lower() for l in self.getAllLangOptions()]:
                name_arr.remove(n)
        name = " ".join(name_arr)
        query = "SELECT Language FROM t"
        cur = self.df.cursor()
        cur.execute(query)
        res = [r[0] for r in cur.fetchall()]
        max = 0
        poset = process.extract(name, res)
        for po in poset:
            score = int(fuzz.token_sort_ratio(name, po[0])) * int(po[1])
            if score > max:
                max = score
        return int(score)

    def getLanguageGap(self, pdt1, pdt2):

        pdtlang1 = self.getAllAvaliableLanguages(pdt1)
        pdtlang2 = self.getAllAvaliableLanguages(pdt2)
        intersect = set(pdtlang1).intersection(set(pdtlang2))
        #first return value is what is extra for set1 and second value what is extra for set2
        return list(set(pdtlang1) - intersect), list(set(pdtlang2) - intersect)


    def isPartOfName(self, n):
        query = "SELECT Language FROM t"
        cur = self.df.cursor()
        cur.execute(query)
        res = [r[0] for r in cur.fetchall()]
        keys = {}
        for name in ((r.lower()) for r in res):
            words = name.strip().split(" ")

            for word in words:
                if word in blacklist:
                    continue
                if word not in keys:
                    keys.setdefault(word, [])
                keys[word].append(name.strip())

        if str(n).lower() not in (k.lower() for k in keys.keys()):
                return False
        return True

    def getAllLangOptions(self):
        query = "pragma table_info(t)"
        cur = self.df.cursor()
        cur.execute(query)
        return [lang[1] for lang in cur.fetchall()[1:]]



PL = ProductLanguageDatabase()
print PL.getMatchScore("AutoKad")