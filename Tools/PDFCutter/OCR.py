# CRS PDF Files

import pytesseract as pyt
import os.path as osp
import inspect
import re
import nltk.corpus
from pdf2image import convert_from_path


class OCRHanlder:

    # Handels the OCR-File

    def __init__(self):
        self.stopWords = set(nltk.corpus.stopwords.words("german"))
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        FilePath = osp.dirname(osp.abspath(filename))
        #  self.PopplerPath = Path(FilePath + r"\venv\poppler-22.01.0\Library\bin")
        pyt.pytesseract.tesseract_cmd = (FilePath + r'\Tesseract-OCR\tesseract.exe')
        self.DataOfPage = list()
        self.TokensOfPage = list()

    def GetTokenForPage(self, pageNr):
        # OCR alle Pages to List of Tupels
        if self.DataOfPage is not None:
            return self.TokensOfPage[pageNr]
        return None

    def GetDataForPage(self, pageNr):
        # OCR alle Pages to List of Tupel
        if self.DataOfPage is not None:
            return self.DataOfPage[pageNr]
        return None

    def NrOfPages(self):
        # OCR alle Pages to List of Tupels

        if self.DataOfPage is not None:
            return len(self.DataOfPage)

    def OCRFile(self, PDFPath):
        # OCR alle Pages to List of Data

        self.ImgOfPDF = convert_from_path(PDFPath, dpi=350,  fmt="jpeg", poppler_path="venv/poppler-22.04.0/Library/bin")
        self.DataOfPage.clear()
        self.TokensOfPage.clear()
        for Page in self.ImgOfPDF:
            PageData = pyt.image_to_data(Page, output_type=pyt.Output.DICT, lang='deu')
            self.DataOfPage.append(PageData)
            self.TokensOfPage.append(self.cleanTokens(PageData['text'].copy()))

    def cleanTokens(self, allTokens):

        # Remove unnecessary Token from the list for better analysation

        for Token in allTokens:
            if (not bool(re.search('[a-zA-Z\d]', Token))) or (len(Token) < 3) or (Token in self.stopWords):  # \d ist bei re eine ziffer
                allTokens.remove(Token)
        return allTokens
