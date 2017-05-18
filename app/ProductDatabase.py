import csv, sqlite3

class ProductLanguageDatabase:
    def __init__(self, path = '/home/james/PycharmProjects/flaskChatbot/database/db.csv'):

        con = sqlite3.connect(":memory:")
        con.text_factory = str

        cur = con.cursor()
        cur.execute(
            "CREATE TABLE t (Language, French, Italian, German, Spanish, Japanese, Korean, Simplified_Chinese, Tranditional_Chinese, Czech, "
            "Hungarian, Russian, Polish, Brazilian_Portuguese, Danish, Finnish, Dutch, Norwegian"
            ",Swedish,  Romanian, Portuguese, Arabic, Hindi, Indonesian, Thai, Turkish, "
            "Vietnamese, Hebrew);")  # use your column names here

        with open(path,'rb') as fin:  # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['Count of Language'], i['French'], i['Italian'], i['German'], i['Spanish'], i['Japanese'],
                      i['Korean'], i['Simplified Chinese'],
                      i['Tranditional Chinese'], i['Czech'], i['Hungarian'], i['Russian'], i['Polish'],
                      i['Brazilian Portuguese'], i['Danish'],
                      i['Finnish'], i['Dutch'], i['Norwegian'], i['Swedish'], i['Romanian'], i['Portuguese'], i['Arabic'],
                      i['Hindi'], i['Indonesian'], i['Thai'], i['Turkish'], i['Vietnamese'], i['Hebrew']) for i in dr]

        cur.executemany(
            "INSERT INTO t (Language, French, Italian, German, Spanish, Japanese, Korean, Simplified_Chinese, Tranditional_Chinese, Czech, "
            "Hungarian, Russian, Polish, Brazilian_Portuguese, Danish, Finnish, Dutch, Norwegian"
            ",Swedish,  Romanian, Portuguese, Arabic, Hindi, Indonesian, Thai, Turkish, "
            "Vietnamese, Hebrew) VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
            to_db)
        con.commit()
        # con.close()
        self.df = con

    def checkLanguageAvaliability(self, product, language):
        #Is Autocad 360 avaliable in French?, return boolean
        query = "SELECT " + language + "FROM t WHERE Language = '" + product + "'"
        cur = self.df.cursor()
        cur.execute(query)
        assert len(cur.fetchall()) != 0
        return float(cur.fetchall()[0][0]) == 0

    def getAllUnavaliableProducts(self, language):
        #What are the products avaliable in French?
        query = "SELECT Language FROM t WHERE " + language + " IS NULL OR " + language + " = ''"
        cur = self.df.cursor()
        cur.execute(query)
        print cur.fetchall()

    def getAllAvaliableLanguages(self, product):
        #TODO
        #query = "SELECT Language FROM t WHERE Language = '" + product + "'"
        cur = self.df.cursor()
        cur.execute(query)
        print cur.fetchall()

    def isProduct(self, name):
        query = "SELECT Language FROM t WHERE Language = '" + name + "'"
        cur = self.df.cursor()
        cur.execute(query)
        res = cur.fetchall()
        if len(res) == 0:
            return False
        else:
            return True


