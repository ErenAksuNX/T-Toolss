# Handels the SonstigeDokumente

from Tools.PDFCutter.Validater import Validater
from Tools.PDFCutter.DateTimeSearcher import DatetimeSearcher


class SonstigeDocHandler:
    def __init__(self):
        self.Vali = Validater()
        self.DateS = DatetimeSearcher()
        self.AllBefgundZettelIdent = ['befundarbeitn', 'befundzettel', 'befundarbeiten']

    def IsThisSonstigeDokumentBeImported(self, allTokens):

        # Checks if Page can be ignored

        allTokens = self.Vali.lowercastTokens(allTokens)
        for BefundIdent in self.AllBefgundZettelIdent:
            if BefundIdent in allTokens:
                return False
        return True

    def getSonstigeDokumentName(self, allTokens):
        # Handels Sonstige Documents
        return 'SonstigeDokumente'
