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
        #List Flags has different scenarios:
        listFlags = {'hasBE': False, 'hasDO': False, 'hasWRB': False}
        listNN = ("NN", "NNP", "NNS")
        listVB = ("VB", "VBD","VBN", "VP", "VBZ", "VBP")
        listBE = ("is", "are", "were", "was", "am")
        listDO = ("do", "did", "does", "done")
        skip = 0
        #Mark out product names and languages
        for i in range(0, len(self.posList)):
            if pdb.isPartOfName(self.posList[i][0]):
                self.posList[i] = (self.posList[i][0], u'NN')
            if self.posList[i][0].lower() in [l.lower() for l in pdb.getAllLangOptions()]:
                self.posList[i] = (self.posList[i][0], u'NN')


        for i in range(0, len(self.posList)):
            #Handle Skip command
            if skip:
                skip -= 1
                continue

            #Intent: Asking about which aspect
            #Topic: Target of the question


            if  i < len(self.posList)-1 and self.posList[i][1] == "WRB" and self.posList[i+1][1] == "RB" and i < 2:
                listFlags['hasWRB'] == True
                self.intent.append(self.posList[i][0] + " " + self.posList[i+1][0])

            elif listFlags['hasWRB'] == True and listFlags['hasBE'] == True and (self.posList[i][1] == "VBG" or self.posList[i][1] == "VBN"):
                self.action.append(self.posList[i][0])

                # WRB: When, where etc. , how many locales
            elif self.posList[i][1] == "WRB" and self.posList[i + 1][1] == "JJ" and (
                self.posList[i + 2][1] in listNN) and i < len(self.posList) - 2 and i < 2:
                listFlags['hasWRB'] == True
                self.intent.append(self.posList[i][0] + " " + self.posList[i + 1][0])
                j = i + 2
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j = j + 1
                self.enquiryfield.append(enquiry)
                skip = j - i

            # How many
            elif  i < len(self.posList)-1 and self.posList[i][1] == "WRB" and self.posList[i+1][1] == "JJ" and i < 2:
                listFlags['hasWRB'] == True
                self.intent.append(self.posList[i][0] + " " + self.posList[i+1][0])
                skip = 1

            #C23 deleted
            #In English/In Chinese etc
            elif i < len(self.posList)-1 and self.posList[i][1] == "IN" and (self.posList[i][0].lower() in [l.lower() for l in pdb.getAllLangOptions()]):
                self.subject.append(self.posList[i+1][0])

            #When is AutoCAD releasing? /How many languages are AutoCAD released in?(Be verb with product name
            elif i <= 3 and self.posList[i][0].lower() in listBE and i < len(self.posList)-1 and self.posList[i+1][1]in listNN:
                listFlags['hasBE'] = True
                self.intent.append(self.posList[i][0])
                j = i + 1
                subject = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    subject = subject + self.posList[j][0] + " "
                    j = j + 1
                j = j - 1
                self.subject.append(subject)
                skip = j - i
                if self.posList[j+1][1] == "JJ" or self.posList[j+1][1] == "VBN" or self.posList[j+1][1] == "VBD":
                    self.action.append(self.posList[j+1][0])
                    skip = skip + 1
            #MD: Could, Would, will etc. Modal + Noun Phrases: Will Autocad be released in May? In this case, Autocad is the enquiry
            elif i < 3 and self.posList[i][0] == "MD" and i < len(self.posList) - 1 and (self.posList[i+1][0] in listNN):
                self.enquiryfield.append(self.posList[i+1][1])
                skip = 1

            #How many + product name
            elif self.posList[i][1] == "WRB" and self.posList[i+1][1] == "JJ" and (self.posList[i+2][1] == 'PDT') and i < len(self.posList)-2 and i < 2:
                self.intent.append(self.posList[i][0] + " " + self.posList[i+1][0])
                j = i+2
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] == 'PDT')):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i

            #WP: Who, what + verb: Who took my cheese? Who took away his meaning of life?
            elif self.posList[i][1] == "WP" and self.posList[i+1][1] in listVB and (self.posList[i+2][1] == "DT" or self.posList[i+2][1] == 'PRP$') and (self.posList[i+3][1] in listNN) and i < len(self.posList)-3 and i < 2:
                self.intent.append(self.posList[i][0])
                self.action.append(self.posList[i+1][0])
                j = i + 3
                enquiry = ""
                if self.posList[j][1] in listNN:
                    while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                        enquiry = enquiry + self.posList[j][0] + " "
                        j=j+1
                    self.enquiryfield.append(enquiry)
                    skip = j - i
            #What languages does Autocad support?
            elif self.posList[i][1] == "WP" and self.posList[i+1][1] in listNN and self.posList[i+2][1] in listBE and i < len(self.posList)-1:
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
                self.intent.append(self.posList[i][0])
                j = i+1
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i

            #What languages does Autocad support?
            elif self.posList[i][1] == "WDT" and self.posList[i+1][1] in listNN and i < len(self.posList)-1:
                self.intent.append(self.posList[i][0])
                j = i+1
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i

            #I want to know how often does the product renew?
            elif i < len(self.posList) - 3 and self.posList[i][1] == "VB" and self.posList[i+1][1] == "WRB" and self.posList[i+2][1] == "RB" and (self.posList[i+3][1] in listNN):
                self.intent.append(self.posList[i+1][0] + " " + self.posList[i + 3][0])
                j = i+3
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i

            #Handle clauses: I want to know how much effort can you putt in?
            elif i < len(self.posList) - 3 and self.posList[i][1] == "VB" and self.posList[i+1][1] == "WRB" and self.posList[i+2][1] == "JJ" and (self.posList[i+3][1] in listNN):
                self.intent.append(self.posList[i+1][0] + " " + self.posList[i + 2][0])
                j = i+3
                enquiry = ""
                while (j < len(self.posList) and (self.posList[j][1] in listNN)):
                    enquiry = enquiry + self.posList[j][0] + " "
                    j=j+1
                self.enquiryfield.append(enquiry)
                skip = j - i

            #Clauses with no noun phrases
            elif i < len(self.posList) - 2 and self.posList[i][1] == "VB" and self.posList[i+1][1] == "WRB" and self.posList[i+2][1] == "RB":
                self.intent.append(self.posList[i+1][0] + " " + self.posList[i + 2][0])
            elif i < len(self.posList) - 2 and self.posList[i][1] == "VB" and self.posList[i+1][1] == "WRB" and self.posList[i+2][1] == "JJ":
                self.intent.append(self.posList[i+1][0] + " " + self.posList[i + 2][0])

            #How much more do you want? (Without noun at the back)
            elif self.posList[i][1] == "WRB" and self.posList[i+1][1] == "JJ" and i < len(self.posList)-1 and i < 2:
                self.intent.append(self.posList[i][0] + " " + self.posList[i+1][0])


            elif self.posList[i][1] == "WRB" and i < 2:
                print "C"
                listFlags['hasWRB'] = True
                self.intent.append(self.posList[i][0])

            elif self.posList[i][1] == "WP" and i < 2:
                self.intent.append(self.posList[i][0])

            elif self.posList[i][1] == "WDT" and self.posList[i+1][1] in listNN and i < len(self.posList) and i < 2:
                self.intent.append(self.posList[i][0])
                self.enquiryfield.append(self.posList[i+1][0])

            elif self.posList[i][1] == "WDT" and i < 2:
                self.intent.append(self.posList[i][0])

            elif i > 0 and self.posList[i - 1][1] == "IN" and self.posList[i][1] == "VBG":
                self.action.append(self.posList[i][0])

            elif self.posList[i][1] in listVB :
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

