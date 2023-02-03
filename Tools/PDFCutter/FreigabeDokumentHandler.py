# Handels the FreigabeDokument

from Tools.PDFCutter.Validater import Validater
from Tools.PDFCutter.DateTimeSearcher import DatetimeSearcher


def nullstring(dateTime):
    if dateTime is not None and dateTime == 0:
        return "00"
    elif dateTime is not None and dateTime < 10:
        return "0" + str(dateTime)
    elif dateTime is not None:
        return str(dateTime)


class ReleaseDocHandler:
    def __init__(self):
        self.Vali = Validater()
        self.FD = 'Freigabedokument'
        self.FreigabeDokumentList = ['qualitäts-produktnachweis', 'arbeitsverzeichnis', 'wiederinbetriebnahme',
                                     'auftragsquittung', 'betriebsfreigabe']
        self.Bretriebsfreigabe = 'betriebsfreigabe'

    def getFreigabeDokumentName(self, allTokens):

        # AllTokens: All Words of the Page in a Tokenized form.
        # Return the Name of the 'FreigabeDokument'

        self.Tokens = allTokens
        DS = DatetimeSearcher()
        Date = DS.findLatesDateTimeFullYear(allTokens)
        time = DS.findLatesTime(allTokens)

        # What Kind of Document is ist

        Fahrzeugnummer = self.Vali.getShortZugNummer(allTokens)  # Auftragsquittung
        if Date is not None and Fahrzeugnummer is not None and self.isBetriebsfreigabe(self.Tokens) and time is not None:
            ReleaseDocName = 'GN_' + Fahrzeugnummer + '_' + str(Date.year) + "-" + nullstring(Date.month) + "-" + nullstring(Date.day) + "-" + nullstring(time.hour) + nullstring(time.minute) + nullstring(time.second)
            return ReleaseDocName
        return self.FD

    def isPageFreigabeDokument(self, pageName):

        # Returns Ture if the PageName belongs to a 'FreigabeDokument'

        if self.FD in pageName or self.isDefinedName(pageName):
            return True
        return False

    def specifieUnpecifiedDoc(self, DestinationFiles, UnspecifiedPage):

        # Tries to returns a specified Name for the 'Freigabdokument'
        # DestinationFiles: List of all DestinationFilenNames
        # UnspecifiedPage: Name of the currently unspecified Freigabdokument.

        DefinedPage = ''
        for Page in DestinationFiles:
            if self.isDefinedName(Page):
                if DefinedPage == '':
                    DefinedPage = Page
                elif DefinedPage != Page:
                    return UnspecifiedPage
        return DefinedPage

    def isDefinedName(self, PageName):

        # Checks if the Dokument ist a 'FreigabeDokument' which is specified.

        PageNameParts = PageName.split('_')

        if (len(PageNameParts) != 3 or
                not PageNameParts[0] == 'GN' or
                not self.Vali.isZugNr(PageNameParts[1]) or
                not len(PageNameParts[2]) == 17):
            return False
        return True

    def isDate (self, parts):

        for date in parts:
            if not date.isnumeric():
                return False
        return True

    def isFreigabeDokument(self, multipleTokens):
        # Checks if this Page is one of the Pages which belong to the ReleaseDocuments
        multipleTokens = self.Vali.lowercastTokens(multipleTokens)
        if len(set(self.FreigabeDokumentList) - set(multipleTokens)) != len(self.FreigabeDokumentList):
            return True

    def isBetriebsfreigabe(self, multipleTokens):
        multipleTokens = self.Vali.lowercastTokens(multipleTokens)
        if self.Bretriebsfreigabe in multipleTokens:
            return True
