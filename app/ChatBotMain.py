import POSTagger
import WordDatabase
import POSToken as POST
import POSProcessor as PP
import re
import enchant
import ProductDatabase
#list of ques:
#1. I want to localize Autocad.

isRunning = True
tagger = POSTagger.POSTagger()
WD = WordDatabase.WordDatabase()
if __name__ == "__main__":
    dic = enchant.Dict("en_US")
    symbol = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"
    prod_db = ProductDatabase.ProductLanguageDatabase()
    while(isRunning):
        line = raw_input("Please enter your line below: ")
        linecpy = line
        for ch in linecpy:
            if ch in symbol:
                linecpy.replace(ch, '')
        linecpy = re.sub('[^0-9a-zA-Z ]+', '', linecpy)
        lineArr = linecpy.split(" ")
        for i in range(0, len(lineArr)):
            if prod_db.isPartOfName(lineArr[i]):
                sug = lineArr[i]
            else:
                sug = dic.suggest(lineArr[i])[0]
        lineArr = [sug if x==lineArr[i] else x for x in lineArr]
        str = ' '.join(lineArr)

        pos = tagger.parse(str)
        proc = PP.Processor(pos)
        proc.posTokenGen()
        proc.printOutput()

        pro = POST.Token(proc.getIntent(), proc.getSubject(), proc.getAction(), proc.getEnquires())
        print pro.process()



