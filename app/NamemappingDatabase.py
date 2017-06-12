import csv, sqlite3

class NameDatabase:
    def __init__(self, path='/home/james/PycharmProjects/flaskChatbot/database/name_mapping.csv'):
        con = sqlite3.connect(":memory:")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("CREATE TABLE t (Localized_Product_Matrix, Related_NPI_Product);")
        with open(path,'rb') as fin:  # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin)  # comma is default delimiter
            to_db = [(i['Localized Product Matrix'], i['Related NPI Product']) for i in dr]
        cur.executemany(
            "INSERT INTO t (Localized_Product_Matrix, Related_NPI_Product) VALUES (?, ?);",
            to_db)
        con.commit()
        self.df = con


    def mapping(self, name):
        query = "SELECT Related_NPI_Product FROM t WHERE UPPER(Localized_Product_Matrix) = '" + name.upper() + "';"
        print query
        cur = self.df.cursor()
        cur.execute(query)
        res = cur.fetchall()
        try:
            if res[0][0] == "No":
                return name
            else:
                return res[0][0]
        except Exception:
            return name

