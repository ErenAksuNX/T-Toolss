
# Handels the Übergabeprotokoll

from Tools.PDFCutter.Validater import Validater
from Tools.PDFCutter.DateTimeSearcher import *


class UebergabeProtokollHandler:
    def __init__(self):
        self.datum = None
        self.Vali = Validater()
        self.DateS = DatetimeSearcher()

    def getUebergabeProtocolName(self, allTokens):

        # Handels Sonstige Documents

        Date = self.DateS.findLatestDateTimeBouthFormats(allTokens)
        Fahrzeugnummer = self.Vali.getShortZugNummer(allTokens)
        self.datum = None
        
        if Date is not None:            
            self.datum = str(Date.year) + nullstring(Date.month) + nullstring(Date.day)
    
        if Fahrzeugnummer is None:
            Fahrzeugnummer = self.Vali.getShortZugNummer(allTokens)

        if Date is not None and Fahrzeugnummer is not None:
            ReleaseDocName = Fahrzeugnummer + '_' + self.datum + '_' + 'Übergabeprotokoll'
        else:
            ReleaseDocName = 'Übergabeprotokoll'
        return ReleaseDocName

    def isUebergabeProtokoll(self, multipleTokens):

        # Checks if the word 'Produktnachweis' is in the Document

        multipleTokens = self.Vali.lowercastTokens(multipleTokens)
        if 'fahrzeugübergabe' in multipleTokens:
            return True
        return False
