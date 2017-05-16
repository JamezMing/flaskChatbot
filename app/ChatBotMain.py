import POSTagger
import WordDatabase
import POSToken as POST
import POSProcessor as PP
import enchant
#list of ques:
#1. I want to localize Autocad.

isRunning = True
tagger = POSTagger.POSTagger()
WD = WordDatabase.WordDatabase()
if __name__ == "__main__":
    dic = enchant.Dict("en_US")
    symbol = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"
    while(isRunning):
        line = raw_input("Please enter your line below: ")
        print line
        linecpy = line
        for ch in linecpy:
            if ch in symbol:
                linecpy.replace(ch, '')
        lineArr = linecpy.split(" ")
        for i in range(0, len(lineArr)):
            if dic.check(lineArr[i]) == False:
                if len(WD.isProduct(lineArr[i])) != 0:
                    if i + 1 < lineArr:
                        w = lineArr[i] + " " + lineArr[i+1]
                        if len(WD.isProduct(w)) != 0:
                            sug = w
                            continue
                    sug = WD.isProduct(lineArr[i])[0]
                    print sug
                else:
                    sug = dic.suggest(lineArr[i])[0]
                lineArr = [sug if x==lineArr[i] else x for x in lineArr]
        str = ' '.join(lineArr)

        print str
        pos = tagger.parse(str)
        proc = PP.Processor(pos)
        proc.posTokenGen()
        proc.printOutput()

        pro = POST.Token(proc.getIntent(), proc.getSubject(), proc.getAction(), proc.getEnquires())



