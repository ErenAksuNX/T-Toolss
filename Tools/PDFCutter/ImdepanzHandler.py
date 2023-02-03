from Tools.PDFCutter.Validater import Validater
from Tools.PDFCutter.DateTimeSearcher import DatetimeSearcher


class ImdepanzHandler:

    def __init__(self):
        self.Vali = Validater()
        self.DateS = DatetimeSearcher()
        self.ImdepanzIdentifier = ['tür-schließkraftmessung', 'Türtyp', ]

    def IsThisaIHProtokoll(self, AllTokens):
        # Checks if Page is a PZB document

        AllTokens = self.Vali.lowercastTokens(AllTokens)
        if len(set(self.ImdepanzIdentifier) - set(AllTokens)) == 0:
            return True
        return False

    def getIHDokumentName(self, AllTokens):

        # Handels PZB Documents

        Date = self.DateS.findLatestDateTimeBouthFormats(AllTokens)
        Fahrzeugnummer = self.Vali.getShortZugNummer(AllTokens)
        if Fahrzeugnummer is None:
            Fahrzeugnummer = self.Vali.getFzNummerShort(AllTokens)
        if Date is not None and Fahrzeugnummer is not None:
            ReleaseDocName = Fahrzeugnummer + '_' + str(Date.year) + str(Date.month) + str(Date.day) + '_' + 'Impedanz'
        else:
            ReleaseDocName = 'ImdepanzDokument'
        return ReleaseDocName

    def isDefinedName(self, PageName):

        # Checks if the Dokument ist a 'LVADokument' which is specified.

        PageNameParts = PageName.split('_')
        if ((len(PageNameParts) != 3 or
             not self.Vali.isZugNr(PageNameParts[0]) or
             not (len(PageNameParts[1]) <= 8 and len(PageNameParts[1]) >= 6) or
             not PageNameParts[1].isnumeric()) or
                not PageNameParts[2] == 'Impedanz'):
            return False
        return True

    def specifieUnpecifiedDoc(self, DestinationFiles, UnspecifiedPage):

        # Tries to returns a specified Name for the 'PZB'
        # DestinationFiles: List of al DestinationFilenNames
        # UnspecifiedPage: Name of the currently unspecified Freigabdokument.

        DefinedPage = ''
        for Page in DestinationFiles:
            if self.isDefinedName(Page):
                if DefinedPage == '':
                    DefinedPage = Page
                elif DefinedPage != Page:
                    return UnspecifiedPage
        return DefinedPage

