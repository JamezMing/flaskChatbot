import POSTagger
import WordDatabase
import POSProcessor
import POSToken
import enchant

class Processor:
    def __init__(self, path_tagger = "/home/james/Downloads/stanford-postagger-full-2016-10-31/stanford-postagger.jar"):
        self.POSTagger = POSTagger.POSTagger(path_to_jar=path_tagger)
        self.Dict = enchant.Dict("en_US")
        self.Database = WordDatabase.WordDatabase()
        self.Symbolset  = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"

    def process_line(self, line):
        for ch in line:
            if ch in self.Symbolset:
                line.replace(ch, '')
        lineArr = line.split(" ")
        for i in range(0, len(lineArr)):
            if self.Dict.check(lineArr[i]) == False:
                if len(self.Database.isProduct(lineArr[i])) != 0:
                    if i + 1 < lineArr:
                        w = lineArr[i] + " " + lineArr[i+1]
                        if len(self.Database.isProduct(w)) != 0:
                            sug = w
                            continue
                    sug = self.Database.isProduct(lineArr[i])[0]
                    print sug
                else:
                    sug = self.Dict.suggest(lineArr[i])[0]
                lineArr = [sug if x==lineArr[i] else x for x in lineArr]
        str = ' '.join(lineArr)
        pos = self.POSTagger.parse(str)
        proc = POSProcessor.Processor(pos)
        proc.posTokenGen()
        postoken = POSToken.Token(proc.getIntent(), proc.getSubject(), proc.getAction(), proc.getEnquires())
        ans = postoken.process()
        return ans

