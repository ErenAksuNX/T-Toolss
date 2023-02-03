# Handels the Analysation
import os.path

from Tools.PDFCutter.OCR import OCRHanlder
from Tools.PDFCutter.PDFHandler import PDFHandler
from Tools.PDFCutter.ArbeitsscheinHandler import ArbeitsscheinHandler
from Tools.PDFCutter.FreigabeDokumentHandler import ReleaseDocHandler
from Tools.PDFCutter.SonstigeDokumenteHandler import SonstigeDocHandler
from Tools.PDFCutter.UebergabeprotokollHandler import UebergabeProtokollHandler
from Tools.PDFCutter.UFDProtokollHandler import UFDProtokollHandler
from Tools.PDFCutter.PZBProtokollHandler import PZBDocHandler
from Tools.PDFCutter.BRHandler import BrDocHandler
from Tools.PDFCutter.LVAHandler import LVADocHandler
from Tools.PDFCutter.Turhandler import TurHandler
from Tools.PDFCutter.TCLHandler import *
from Tools.PDFCutter.ImdepanzHandler import *
from tkinter.messagebox import *


class AnalyseHandler:
    def __init__(self, PDFFiles, destination):

        # Sets up the File which Analyses and sets up Destination Path Folder.

        self.PDFOriginal = PDFFiles
        self.DestinationPath = destination
        self.AH = ArbeitsscheinHandler()
        self.FH = ReleaseDocHandler()
        self.SDH = SonstigeDocHandler()
        self.Vali = Validater()
        self.OCRH = OCRHanlder()
        self.UPH = UebergabeProtokollHandler()
        self.UFDP = UFDProtokollHandler()
        self.PZB = PZBDocHandler()
        self.BRH = BrDocHandler()
        self.LVAH = LVADocHandler()
        self.TH = TurHandler()
        self.TCL = TCLHandler()
        self.IH = ImdepanzHandler()

    def run(self):

        # OCRs the PDF and Analyses the File afterward

        for file in self.PDFOriginal:
            DestinationFiles = list()
            PDFH = PDFHandler(self.DestinationPath)
            self.OCRH.OCRFile(file)
            for Nr in range(self.OCRH.NrOfPages()):
                PageName = self.analysePage(Nr)
                PageName = self.addOrgFilenameIfNecesarry(PageName, os.path.basename(file))
                DestinationFiles.append(PageName)
            DestinationFiles = self.AssignPageInformationsFromOtherPages(DestinationFiles)
            PDFH.run(file, DestinationFiles)
            DestinationFiles.clear()

        showinfo('Info', 'Die Analyse wurde beendet')

    def analysePage(self, pageNr):

        # Analyses the single Page and returns the PageName
        # PageNr: The Number of the Page

        Tokens = self.OCRH.GetTokenForPage(pageNr)
        if self.AH.isArbeitsschein(Tokens):
            return self.AH.getArbeitsscheinName(self.OCRH.GetDataForPage(pageNr))
        elif self.FH.isFreigabeDokument(Tokens):
            return self.FH.getFreigabeDokumentName(Tokens)
        elif self.UPH.isUebergabeProtokoll(Tokens):
            return self.UPH.getUebergabeProtocolName(Tokens)
        elif self.UFDP.isUFDProtokoll(Tokens):
            return self.UFDP.getUFDProtocolName(Tokens)
        elif self.PZB.IsThisaPZBProtokoll(Tokens):
            return self.PZB.getPZBDokumentName(Tokens)
        elif self.BRH.isBrDokument(Tokens):
            return self.BRH.getBrDokumentName(Tokens)
        elif self.LVAH.IsThisaLVAProtokoll(Tokens):
            return self.LVAH.getLVADokumentName(Tokens)
        elif self.TH.IsThisaTurProtokoll(Tokens):
            return self.TH.getTurDokumentName(Tokens)
        elif self.TCL.IsThisaTclProtokoll(Tokens):
            return self.TCL.getTCLDokumentName(Tokens)
        elif self.IH.IsThisaIHProtokoll(Tokens):
            return self.IH.getIHDokumentName(Tokens)
        elif self.SDH.IsThisSonstigeDokumentBeImported(Tokens):
            return self.SDH.getSonstigeDokumentName(Tokens)
        else:
            return 'IgnorePage'

    def addOrgFilenameIfNecesarry(self, pageName, filename):

        # If not clear add Orgginal Filanem to Destination file.
        # PageName: Name of the DestinationFile
        # Filename: Name of the Org File

        if self.Vali.isPageNameNotDefined(pageName):
            return pageName + '_' + filename.split(".pdf")[0] # er erkennt den arbeitsschein nicht richtig
        else:
            return pageName

    def AssignPageInformationsFromOtherPages(self, destinationFiles):

        # DestinationFiles : Name of all Files which are the PageDestination

        for idx, page in enumerate(destinationFiles): # Fehlerquelle
            if self.Vali.isPageNameNotDefined(page):
                if self.AH.isPageArbeitsschein(page):
                    destinationFiles[idx] = self.AH.specifieUnspecifiedDoc(destinationFiles, page)
                elif self.FH.isPageFreigabeDokument(page):
                    destinationFiles[idx] = self.FH.specifieUnpecifiedDoc(destinationFiles, page)
                elif self.UFDP.isPageNameUFDProtokoll(page):
                    destinationFiles[idx] = self.UFDP.specifieUnpecifiedDoc(destinationFiles, page)
                elif self.PZB.IsThisaPZBProtokoll(page):
                    destinationFiles[idx] = self.PZB.specifieUnpecifiedDoc(destinationFiles, page)
                elif self.BRH.isBrDokument(page):
                    destinationFiles[idx] = self.BRH.specifieUnpecifiedDoc(destinationFiles, page)
                elif self.LVAH.IsThisaLVAProtokoll(page):
                    destinationFiles[idx] = self.LVAH.specifieUnpecifiedDoc(destinationFiles, page)
                elif self.TCL.IsThisaTclProtokoll(page):
                    destinationFiles[idx] = self.TCL.specifieUnpecifiedDoc(destinationFiles, page)
                elif self.TH.IsThisaTurProtokoll(page):
                    destinationFiles[idx] = self.TH.specifieUnpecifiedDoc(destinationFiles, page)
                elif self.IH.IsThisaIHProtokoll(page):
                    destinationFiles[idx] = self.IH.specifieUnpecifiedDoc(destinationFiles, page)

        return destinationFiles
