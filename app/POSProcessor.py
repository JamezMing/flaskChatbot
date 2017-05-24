from nltk.tag import StanfordPOSTagger
from ProductDatabase import ProductLanguageDatabase
import nltk

class Processor:
    def __init__(self, poslist):
        self.posList = poslist
        self.actObjPairs = list()
        self.action = list()
        self.subject = list()
        self.enquiryfield = list()
        self.intent = list()
        self.connector = list()
        self.negate = False

    def posTokenGen(self):
        pdb = ProductLanguageDatabase()
        listFlags = list()
        listNN = ("NN", "NNP", "NNS")
        listVB = ("VB", "VBD","VBN", "VP", "VBZ", "VBP")
        listBE = ("is", "are", "were", "was", "am")
        listNeg = ("not", "n't")
        skip = 0
        for i in range(0, len(self.posList)):
            if pdb.isPartOfName(self.posList[i][0]):
                self.posList[i] = (self.posList[i][0], u'NN')

        for i in range(0, len(self.posList)):
            if self.posList[i][1] in listVB and i < len(self.posList)-1 and self.posList[i+1][1] == "RB" and self.posList[i+1][0] in listNeg:
                self.negate = not self.negate
            if skip:
                skip -= 1
                continue
            if self.posList[i][1] == "WRB" and self.posList[i+1][1] == "RB" and i < len(self.posList)-1 and i < 2:
                print "C0"
                self.intent.append(self.posList[i][0] + " " + self.posList[i+1][0])

            elif "WRB" in listFlags and "BE" in listFlags and self.posList[i][1] == "VBG":
                print "C23"
                self.action.append(self.posList[i][0])

            elif i < len(self.posList)-1 and self.posList[i][1] == "IN" and ((self.posList[i+1][0].lower()) in [u.lower() for u in pdb.getAllLangOptions()]):
                self.subject.append(self.posList[i+1][0])

            elif i < 2 and self.posList[i][0].lower() in listBE and i < len(self.posList)-1 and self.posList[i+1][1] in listNN:
                print "C1"
                listFlags.append("BE")
                self.intent.append(self.posList[i][0])
                j = i + 1
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j = j + 1
                j = j - 1
                self.enquiryfield.append(enquiry)
                skip = j - i
                if self.posList[j+1][1] == "JJ" or self.posList[j+1][1] == "VBN":
                    self.intent.append(self.posList[j+1][0])
                    skip = skip + 1

            elif i < 3 and self.posList[i][0] == "MD" and i < len(self.posList) - 1 and self.posList[i+1][0] == "NNP":
                self.enquiryfield.append(self.posList[i+1][1])
                skip = 1

            elif self.posList[i][1] == "WRB" and self.posList[i+1][1] == "JJ" and (self.posList[i+2][1] in listNN) and i < len(self.posList)-2 and i < 2:
                print "C2"
                self.intent.append(self.posList[i][0] + " " + self.posList[i+1][0])
                j = i+2
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i

            elif self.posList[i][1] == "WP" and self.posList[i+1][1] in listVB and self.posList[i+2][1] == "DT" and (self.posList[i+3][1] in listNN) and i < len(self.posList)-3 and i < 2:
                print "C3"
                self.intent.append(self.posList[i][0] + " " + self.posList[i+1][0])
                j = i+3
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i

            elif self.posList[i][1] == "WP" and self.posList[i+1][1] in listNN and self.posList[i+2][1] in listBE and i < len(self.posList)-1:
                print "C4"
                self.intent.append(self.posList[i][0])
                j = i+1
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i

            #I want to know what languages are avaliable for Autocad?
            elif self.posList[i][1] == "WP" and self.posList[i+1][1] in listNN and i < len(self.posList)-1:
                print "C5"
                self.intent.append(self.posList[i][0])
                j = i+1
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i


            elif self.posList[i][1] == "WDT" and self.posList[i+1][1] in listNN and i < len(self.posList)-1:
                print "C6"
                self.intent.append(self.posList[i][0])
                j = i+1
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i


            elif i < len(self.posList) - 3 and self.posList[i][1] == "VB" and self.posList[i+1][1] == "WRB" and self.posList[i+2][1] == "RB" and (self.posList[i+3][1] in listNN):
                print "C7"
                self.intent.append(self.posList[i+1][0] + " " + self.posList[i + 3][0])
                j = i+3
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i
            elif i < len(self.posList) - 3 and self.posList[i][1] == "VB" and self.posList[i+1][1] == "WRB" and self.posList[i+2][1] == "JJ" and (self.posList[i+3][1] in listNN):
                print "C8"
                self.intent.append(self.posList[i+1][0] + " " + self.posList[i + 2][0])
                j = i+3
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i
            elif i < len(self.posList) - 2 and self.posList[i][1] == "VB" and self.posList[i+1][1] == "WRB" and self.posList[i+2][1] == "RB":
                print "C9"
                self.intent.append(self.posList[i+1][0] + " " + self.posList[i + 2][0])
            elif i < len(self.posList) - 2 and self.posList[i][1] == "VB" and self.posList[i+1][1] == "WRB" and self.posList[i+2][1] == "JJ":
                print "C10"
                self.intent.append(self.posList[i+1][0] + " " + self.posList[i + 2][0])
            elif self.posList[i][1] == "WRB" and self.posList[i+1][1] == "JJ" and i < len(self.posList)-1 and i < 2:
                print "C11"
                self.intent.append(self.posList[i][0] + " " + self.posList[i+1][0])
            elif self.posList[i][1] == "WRB" and i < 2:
                listFlags.append("WRB")
                print "C12"
                self.intent.append(self.posList[i][0])
            elif self.posList[i][1] == "WP" and i < 2:
                print "C13"
                self.intent.append(self.posList[i][0])
            elif self.posList[i][1] == "WDT" and self.posList[i+1][1] in listNN and i < len(self.posList) and i < 2:
                print "C14"
                self.intent.append(self.posList[i][0])
                self.enquiryfield.append(self.posList[i+1][0])
            elif self.posList[i][1] == "WDT" and i < 2:
                print "C15"
                self.intent.append(self.posList[i][0])
            elif i > 0 and self.posList[i - 1][1] == "IN" and self.posList[i][1] == "VBG":
                print "C16"
                self.action.append(self.posList[i][0])
            elif self.posList[i][1] in listVB :
                print "C17"
                if self.posList[i][0] in listBE:
                    if self.posList[i+1][1] == "DT":
                        self.action.append(self.posList[i][0])
                    else:
                        for j in range(i, len(self.posList)):
                            if self.posList[j][1] == "JJ" and j < len(self.posList)-1 and self.posList[j+1][1] == "TO" :
                                self.action.append(self.posList[i][0] + " " + self.posList[j][0] + " " + self.posList[j+1][1])
                                break
                            elif self.posList[j][1] == "JJ":
                                self.action.append(self.posList[i][0] + " " + self.posList[j][0])
                                break
                else:
                    self.action.append(self.posList[i][0])
            elif self.posList[i][1] == "NN" and i < len(self.posList) - 2 and self.posList[i + 1][1] == "CC" and self.posList[i + 2][1] == "NN":
                print "C18"
                self.subject.append(self.posList[i][0] + " " + self.posList[i + 1][0] + " " + self.posList[i + 2][0])
            elif self.posList[i][1] in listNN and i < len(self.posList)-1 and self.posList[i+1][1] in listNN:
                print "C19"
                enquiry = self.posList[i][0] + " "
                j = i + 1
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j = j + 1
                self.subject.append(enquiry)
                skip = j - i
            elif self.posList[i][1] in listNN and i < len(self.posList) - 1 and self.posList[i + 1][1] == "CD":
                print "C20"
                self.subject.append(self.posList[i][0] + " " + self.posList[i + 1][0])
            elif self.posList[i][1] in listNN:
                print "C21"
                self.subject.append(self.posList[i][0])
            elif self.posList[i][1] == "NN" and i < len(self.posList)-1 and self.posList[i+1][1] == "CC":
                print "C22"
                self.connector.append(self.posList[i+1][0])

    def getSubject(self):
        return self.subject

    def getAction(self):
        return self.action

    def getIntent(self):
        return self.intent

    def getEnquires(self):
        return self.enquiryfield

    def getNegation(self):
        return self.negate

    def printOutput(self):
        print "Subject: "
        print (self.subject)
        print "Action: "
        print self.action
        print "Intent: "
        print self.intent
        print "Enquiry"
        print self.enquiryfield
        print self.negate

