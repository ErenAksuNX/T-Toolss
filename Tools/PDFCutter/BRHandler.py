# Handels the BRDokumente

from Tools.PDFCutter.Validater import Validater
from Tools.PDFCutter.DateTimeSearcher import DatetimeSearcher


class BrDocHandler:
    def __init__(self):
        self.Vali = Validater()
        self.BR = 'BRDokument'
        self.BrDokumentList = ['dichtheit hl', 'prüfprotokoll br']
        self.Bretriebsfreigabe = 'BR'

    def getBrDokumentName(self, allTokens):

        # AllTokens: All Words of the Page in a Tokenized form.
        # Return the Name of the 'FreigabeDokument'

        self.Tokens = allTokens
        DS = DatetimeSearcher()
        Date = DS.findLatesDateTimeFullYear(allTokens)

        # What Kind of Document is ist

        Fahrzeugnummer = self.Vali.getZugNummerMedium(allTokens)  # Auftragsquittung
        if Date is not None and Fahrzeugnummer is not None:
            ReleaseDocName = 'BR_' + Fahrzeugnummer + '_' + str(Date.year) + str(Date.month) + str(Date.day)
            return ReleaseDocName
        return self.BR

    def isPageBRDokument(self, pageName):

        # Returns Ture if the PageName belongs to a 'FreigabeDokument'

        if self.BR in pageName or self.isDefinedName(pageName):
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

        # Checks if the Dokument ist a 'BrDokument' which is specified.

        PageNameParts = PageName.split('_')
        if (len(PageNameParts) != 3 or
                not PageNameParts[0] == 'BR' or
                not self.Vali.isZugNr(PageNameParts[1]) or
                not (len(PageNameParts[2]) <= 8 and len(PageNameParts[2]) >= 6) or
                not PageNameParts[2].isnumeric()):
            return False
        return True

    def isBrDokument(self, multipleTokens):
        # Checks if this Page is one of the Pages which belong to the ReleaseDocuments
        multipleTokens = self.Vali.lowercastTokens(multipleTokens)
        if len(set(self.BrDokumentList) - set(multipleTokens)) != len(self.BrDokumentList):
            return True
