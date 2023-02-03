# Handels the PDF File

import PyPDF2
from os.path import exists


class PDFHandler:
    def __init__(self, destinationPath):
        self.DestinationPath = destinationPath
        self.ExistingPathFiles = list()
        self.WriterList = list()

    def run(self, fileOrg, pathDesFiles):

        # Is Responsible for Creating the PDFFiles after the pages are assigned.
        # This Function gets executed for each original PDF document

        InfileOrg = open(fileOrg, 'rb')
        InReader = PyPDF2.PdfFileReader(InfileOrg)  # Original PDF document
        for PageCnt, filePath in enumerate(pathDesFiles):
            if filePath != 'IgnorePage':
                if filePath is not None:
                    PathNewFile = str(self.DestinationPath + '/' + filePath + '.pdf')
                    if PathNewFile in self.ExistingPathFiles:
                        self.mergeToExistingFile(PathNewFile, InReader.getPage(PageCnt))
                    else:
                        self.writeNewFile(PathNewFile, InReader.getPage(PageCnt))
        self.createFiles()
        self.WriterList.clear()
        self.ExistingPathFiles.clear()
        InfileOrg.close()

    def writeNewFile(self, pathOutFile, newPage):

        # Creates the New PDF File
        # NewPage = InFile PageOj (.getPage)

        self.WriterList.append(PyPDF2.PdfFileWriter())
        self.WriterList[-1].addPage(newPage)
        self.ExistingPathFiles.append(pathOutFile)

    def createFiles(self):

        # Creates the Output Files

        for idx, Path in enumerate(self.ExistingPathFiles):
            OutFileCnt = 1
            while exists(Path):
                PathWithoutPdf = Path.split('.pdf')
                Path = str(PathWithoutPdf[0] + '_' + str(OutFileCnt) + '.pdf')
                OutFileCnt += 1
            outfileNew = open(Path, 'wb')
            self.WriterList[idx].write(outfileNew)
            outfileNew.close()

    def mergeToExistingFile(self, pathOutFile, newPage):

        # Merge Page To Existing PDf File
        # PathOutFile = PathToPDF FIle
        # NewPage = = InFile PageOj (.getPage

        try:
            for idx, existInPath in enumerate(self.ExistingPathFiles):
                if existInPath == pathOutFile:
                    self.WriterList[idx].addPage(newPage)
        except:
            pass
