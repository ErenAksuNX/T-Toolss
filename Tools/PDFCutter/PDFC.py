from Tools.PDFCutter.Analyser import *

# Die Prozedur um den Analyser aufzurufen

def Analyse(PDFFiles, destination):
    # Start analsation

    AH = AnalyseHandler(PDFFiles, destination)
    AH.run()


class PDF:

    # Im init Block wird nur die Benutzeroberfläche erstellt

    def __init__(self, datei, speicherort):
        self.paths = datei
        self.speicherort = speicherort

    def _getPDFFiles(self, paths):
        # Returns all the Files inside the Folder

        PDFFiles = list()
        PDFFiles.append(paths)
        return PDFFiles

    def start(self):
        Analyse(self._getPDFFiles(self.paths), self.speicherort)
