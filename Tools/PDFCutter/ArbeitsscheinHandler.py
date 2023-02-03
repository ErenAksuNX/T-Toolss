from Tools.PDFCutter.Validater import Validater
from Tools.PDFCutter.DateTimeSearcher import *


class ArbeitsscheinHandler:
    def __init__(self):
        self.AS = 'Arbeitsschein'
        self.As2P = 'Arbeitsschein2Page'
        self.Vali = Validater()
        self.allZGrund = ['ZGRUND', 'Z-GRUND', '2-grund']
        self.Seite = 'Seite'
        self.ZustellungGrund = ['200', '510', '520', '530', '540', '560', '351', '352', '30A', '30B', '30C', '30E',
                                '30F', '31D', '31F', '31R', '31S', '39S', '39O', '39P', '030', '035', '050']
        self.ArbeitsscheinSentence = ['arbeitsauftrag', 'entsprechend', 'regelwerk', 'ordnungsgemäß', 'vollständig']

    def isPageArbeitsschein(self, pageName):

        # Returns True if the PageName belongs to a 'Arbeitsschein'

        if self.AS in pageName or self.isDefinedName(pageName) or self.As2P in pageName:
            return True
        else:
            return False

    def specifieUnspecifiedDoc(self, destinationFiles, unspecifiedPage):

        # Tries to return a specified Name for the 'Arbeitsschein'
        # DestinationFiles: List of all DestinationFileNames
        # UnspecifiedPage: Name of the currently unspecified Page.

        DefinedPage = ''
        if self.As2P in unspecifiedPage:
            for idx, Page in enumerate(destinationFiles):
                if self.As2P in Page:
                    if idx == 0:
                        return 'IgnorePage'
                    if self.isDefinedName(destinationFiles[idx - 1]):
                        return destinationFiles[idx - 1]
            return 'IgnorePage'

        for Page in destinationFiles:
            if self.isDefinedName(Page):
                if DefinedPage == '':
                    DefinedPage = Page
                elif DefinedPage != Page:
                    return unspecifiedPage
        return DefinedPage

    def getArbeitsscheinName(self, pageData):

        # Returns The Name of the 'Arbeitsschein'
        # If The function can not create a Name it just returns Arbeitsschein.

        self.pageData = pageData
        self.tokens = pageData['text']
        self.datum = None

        DS = DatetimeSearcher()
        Date = DS.findEndDateTimeShortYear(self.tokens)
        Fahrzeugnummer = self.Vali.getZugNummer(self.tokens)
        Reason = self.findServiceReason()

        try:
            self.datum = str(Date.year) + nullstring(Date.month) + nullstring(Date.day)
        except:
            pass

        if Date is not None and Fahrzeugnummer is not None and Reason is not None:
            ArbeitsscheinName = Fahrzeugnummer + '_' + self.datum + '_' + Reason
        else:
            ArbeitsscheinName = self.AS
        if self.isPageTwoOfTwo():
            ArbeitsscheinName = self.As2P
        return ArbeitsscheinName

    def findServiceReason(self):

        # This Functions find the Reason for the Service on the 'Arbeitsschein'
        # Nr of the Page

        for ZGrund in self.allZGrund:
            WordsInArea = self.FindZGrund(ZGrund)
            if len(WordsInArea) != 0:
                break
        for Token in WordsInArea:
            if self.isZustellungGrund(Token):
                return Token

    def FindZGrund(self, ZGrund):

        # Returns all Images which are close to a given word around a given PDF
        # PDFPageNr: PDF PageNr
        # Word: CentralWord

        WordList = list()
        for idx, ImgWord in enumerate(self.pageData['text']):
            if ImgWord.upper() == ZGrund.upper():
                x, y, w, h = self.pageData['left'][idx], self.pageData['top'][idx], self.pageData['width'][idx], \
                             self.pageData['height'][idx]
                WordList.clear()
                for idx2, Word in enumerate(self.pageData['text']):
                    LeftDP = self.pageData['left'][idx2]
                    TopDP = self.pageData['top'][idx2]

                    if (x + w) >= LeftDP >= (x - w) and TopDP >= y and TopDP <= (y + (4 * h)):
                        WordList.append(Word)

                return WordList

        return []

    def isDefinedName(self, pageName):

        # Checks if the Dokument ist a 'ArbeitsscheinName' which is defined.

        PageNameParts = pageName.split('_')
        if (len(PageNameParts) != 3 or not self.Vali.isFazNr(PageNameParts[0]) or
                not (8 >= len(PageNameParts[1]) >= 6) or
                not PageNameParts[1].isnumeric() or
                not self.isZustellungGrund(PageNameParts[2])):
            return False
        else:
            return True

    def isArbeitsschein(self, multipleTokens):

        # Checks if the word 'Arbeitsschein' is in the Document

        multipleTokens = self.Vali.lowercastTokens(multipleTokens)
        if ('arbeitsschein' in multipleTokens or
                len(set(self.ArbeitsscheinSentence) - set(multipleTokens)) == 0):
            return True

    def isZustellungGrund(self, token):
        if token in self.ZustellungGrund:
            return True
        return False

    def isPageTwoOfTwo(self):

        # Returns True if page is second As Page

        WordList = list()
        for idx, ImgWord in enumerate(self.pageData['text']):
            if ImgWord.upper() == self.Seite.upper():
                x, y, w, h = self.pageData['left'][idx], self.pageData['top'][idx], self.pageData['width'][idx], \
                             self.pageData['height'][idx]
                WordList.clear()
                for idx2, Word in enumerate(self.pageData['text']):

                    LeftDP = self.pageData['left'][idx2]
                    TopDP = self.pageData['top'][idx2]

                    if LeftDP <= (x + (4 * w)) and LeftDP >= (x - (2 * w)) and TopDP >= (y - (2 * h)) and TopDP <= (y + (4 * h)):
                        WordList.append(Word)

        if WordList.count('2') == 2:
            return True
        return False
