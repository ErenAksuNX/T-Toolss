import datetime
import abc


class FileTypes:
    def __init__(self, name: str, keywords: list, kuerzel: str,frznr: str, datum: datetime.datetime):
        self.name = name
        self.keywords = keywords
        self.kuerzel = kuerzel
        self.frznr = frznr
        self.datum = datum

    @abc.abstractmethod
    def get_export_name(self):
        pass

