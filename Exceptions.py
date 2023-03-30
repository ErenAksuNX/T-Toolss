class PDFExceptions(Exception):
    """Oberklasse für die PDF Exceptions"""
    pass

class NoFileSelected(PDFExceptions):
    """Es wurde keine PDF-Datei ausgewählt"""
    pass

class Wrong_Pages_Input(PDFExceptions):
    """Der Pages String ist nicht gültig"""
    pass

class Page_Count_To_High(PDFExceptions):
    """"Die Page range ist höher als die PDF-File seiten hat"""
    pass

class Page_Exists(PDFExceptions):
    """Der Output name ist vergeben"""