
# Handels the UDFProtokoll

from Tools.PDFCutter.Validater import Validater
from Tools.PDFCutter.DateTimeSearcher import DatetimeSearcher


class UFDProtokollHandler:
    def __init__(self):
        self.Vali = Validater()
        self.DateS = DatetimeSearcher()
        self.UFD = 'UFDProtokoll'
        self.UFDCheckliste = ['ufd', 'checkliste']

    def isPageNameUFDProtokoll(self, PageName):

        # Returns Ture if the PageName belongs to a 'UFDProtokoll'

        if self.UFD in PageName or self.isDefinedName(PageName):
            return True
        return False

    def getUFDProtocolName(self, allTokens):
        # Handels Sonstige Documents
        Date = self.DateS.findLatestDateTimeBouthFormats(allTokens)
        Fahrzeugnummer = self.Vali.getShortZugNummer(allTokens)
        if Fahrzeugnummer is None:
            Fahrzeugnummer = self.Vali.getFzNummerShort(allTokens)
        if Date is not None and Fahrzeugnummer is not None:
            return Fahrzeugnummer + '_' + str(Date.year) + str(Date.month) + str(Date.day) + '_' + 'UFD'
        else:
            return 'UFDProtokoll'


    def specifieUnpecifiedDoc(self, DestinationFiles, UnspecifiedPage):

        # Tries to returns a specified Name for the 'UFD'
        # DestinationFiles: List of all DestinationFileNames
        # UnspecifiedPage: Name of the currently unspecified Freigabdokument.

        DefinedPage = ''
        for Page in DestinationFiles:
            if self.isDefinedName(Page):
                if DefinedPage == '':
                    DefinedPage = Page
                elif DefinedPage != Page:
                    return UnspecifiedPage
        return DefinedPage

    def isDefinedName(self, pageName):

        # Checks if the Dokument ist a 'ArbeitsscheinName' which is defined.

        PageNameParts = pageName.split('_')
        if (len(PageNameParts) != 3 or
                not self.Vali.isFazNr(PageNameParts[0]) or
                not PageNameParts[2] == 'UFD' or
                not (len(PageNameParts[1]) <= 8 and len(PageNameParts[1]) >= 6) or
                not PageNameParts[1].isnumeric()):
            return False
        return True

    def isUFDProtokoll(self, multipleTokens):

        # Checks if the word 'Arbeitsschein' is in the Document

        multipleTokens = self.Vali.lowercastTokens(multipleTokens)
        if ('ufd-duesseldorf' in multipleTokens or
                (len(set(self.UFDCheckliste) - set(multipleTokens)) == 0)):
            return True
        return False
