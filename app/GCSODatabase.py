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
            "CREATE TABLE gcso (Modified, 'Product Line Code', 'Product Line', 'Release Type', Release, 'Media Type',"
            "'Languages Available', 'Fiscal Year', 'RTM Date', 'RTP Date', 'RTW Date', "
            "'FCS Date', 'Quarter');")
        with open(path, 'rb') as fin:  # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['Modified'], i['Product Line Code'], i['Product Line'], i['Release Type'], i['Release'], i['Media Type'],
                      i['Languages-Available'], i['Fiscal Year'], i['RTM Date'],
                      i['RTP Date'], i['RTW Date'], i['FCS Date'], i['Qtr']) for i in dr]
        cur.executemany(
            "INSERT INTO gcso (Modified, 'Product Line Code', 'Product Line', 'Release Type', Release, 'Media Type',"
        "'Languages Available', 'Fiscal Year', 'RTM Date', 'RTP Date', 'RTW Date', "
        "'FCS Date', 'Quarter') VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?, ?);",
            to_db)
        con.commit()
        self.df = con

    def findProduct(self, name):
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
            stats = stats[0]
            projtok = ProjectToken(stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6],stats[7],stats[8],stats[9],stats[10],stats[11], stats[12])
            return projtok


    def findProductLanguage(self, name, language):
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
            stats = stats[0]
            projtok = ProjectToken(stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6],stats[7],stats[8],stats[9],stats[10],stats[11], stats[12])
            return projtok


g= GCSODatabase()
print g.findProduct("AutoCAD").Quarter