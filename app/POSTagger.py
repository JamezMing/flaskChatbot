from nltk.tag import StanfordPOSTagger
import nltk

class POSTagger:
    def __init__(self, path_to_model = "/home/james/Downloads/stanford-postagger-full-2016-10-31/models/english-bidirectional-distsim.tagger", path_to_jar = "/home/james/Downloads/stanford-postagger-full-2016-10-31/stanford-postagger.jar"):
        self.tagger=StanfordPOSTagger(path_to_model, path_to_jar)

    def parse(self, line):
        line = nltk.word_tokenize(line)
        return self.tagger.tag(line)


'''tagger = POSTagger()
while(True):
    str = raw_input("please input: ")
    res =  tagger.parse(str)
    print res'''