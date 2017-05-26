import csv, sqlite3, jellyfish
import ProductDatabase
from ProjectToken import ProjectToken
class GCSODatabase:
    def __init__(self, path = '/home/james/PycharmProjects/flaskChatbot/database/gcso.csv'):
        self.pd = ProductDatabase.ProductLanguageDatabase()
        con = sqlite3.connect(":memory:")
        con.text_factory = str
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE gcso (Modified, 'Product Line Code', 'Product Line', 'Release Type', Release, 'Language Code Name', 'Media Type',"
            "'Languages Available', 'Fiscal Year', 'RTM Date', 'RTP Date', 'RTW Date', "
            "'FCS Date', 'Quarter');")
        with open(path, 'rb') as fin:  # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['Modified'], i['Product Line Code'], i['Product Line'], i['Release Type'], i['Release'], i['Language Code Name'], i['Media Type'],
                      i['Languages-Available'], i['Fiscal Year'], i['RTM Date'],
                      i['RTP Date'], i['RTW Date'], i['FCS Date'], i['Qtr']) for i in dr]
        cur.executemany(
            "INSERT INTO gcso (Modified, 'Product Line Code', 'Product Line', 'Release Type', Release, 'Language Code Name', 'Media Type',"
        "'Languages Available', 'Fiscal Year', 'RTM Date', 'RTP Date', 'RTW Date', "
        "'FCS Date', 'Quarter') VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?, ?);",
            to_db)
        con.commit()
        self.df = con

    def findProduct(self, name):
        query = 'SELECT * FROM gcso WHERE "Product Line" = ' + "'" + name + "'"
        cur = self.df.cursor()
        resList = []
        cur.execute(query)
        stats = cur.fetchall()
        if len((stats)) == 0:
            cpname = "Autodesk " + name
            query = 'SELECT * FROM gcso WHERE "Product Line" = ' + "'" + cpname + "'"
            cur = self.df.cursor()
            cur.execute(query)
            stats = cur.fetchall()
        if len((stats)) == 0:
            name = self.pd.findClosetMatch(name)
            query = 'SELECT * FROM gcso WHERE "Product Line" = ' + "'" + name + "'"
            cur = self.df.cursor()
            cur.execute(query)
            stats = cur.fetchall()
        if len((stats)) == 0:
            name = "Autodesk " + name
            query = 'SELECT * FROM gcso WHERE "Product Line" = ' + "'" + name + "'"
            cur = self.df.cursor()
            cur.execute(query)
            stats = cur.fetchall()
        if len(stats) == 0:
            return None
        else:
            for stat in stats:
                projtok = ProjectToken(stat[0],stat[1],stat[2],stat[3],stat[4],stat[5],stat[6],stat[7],stat[8],stat[9],stat[10],stat[11], stat[12], stat[13])
                resList.append(projtok)
            return resList


    def findProductLanguage(self, name, language):
        resList = []
        query = 'SELECT * FROM gcso WHERE "Product Line" = ' + "'" + name + "'"
        cur = self.df.cursor()
        cur.execute(query)
        stats = cur.fetchall()
        if len((stats)) == 0:
            cpname = "Autodesk " + name
            query = 'SELECT * FROM gcso WHERE "Product Line" = ' + "'" + cpname + "'"
            cur = self.df.cursor()
            cur.execute(query)
            stats = cur.fetchall()
        if len((stats)) == 0:
            name = self.pd.findClosetMatch(name)
            query = 'SELECT * FROM gcso WHERE "Product Line" = ' + "'" + name + "'"
            cur = self.df.cursor()
            cur.execute(query)
            stats = cur.fetchall()
        if len((stats)) == 0:
            name = "Autodesk " + name
            query = 'SELECT * FROM gcso WHERE "Product Line" = ' + "'" + name + "'"
            cur = self.df.cursor()
            cur.execute(query)

            stats = cur.fetchall()
        if len(stats) == 0:
            return None
        else:
            for stat in stats:
                @TODO
                #Add languaguage tag func pls
                projtok = ProjectToken(stat[0],stat[1],stat[2],stat[3],stat[4],stat[5],stat[6],stat[7],stat[8],stat[9],stat[10],stat[11], stat[12], stat[13])
                langCode = projtok.langCodeName.split(", ")
                if language in self.pd.getAllLangOptions():
                    if langCode[0] == "Non-Language Specific"
                print str(projtok.languageAvaliable).split(";#")


g= GCSODatabase()
print g.findProductLanguage("AutoCAD")