# Can search for a Datetime in the File in different Formats

import re
from datetime import datetime


def nullstring(dateTime):
    if dateTime is not None and dateTime == 0:
        return "00"
    elif dateTime is not None and dateTime < 10:
        return "0" + str(dateTime)
    elif dateTime is not None:
        return str(dateTime)


class DatetimeSearcher:

    # Class for Handling the search of a Datetime.

    def __init__(self):
        pass

    def findEndDateTimeShortYear(self, allTokens):
        # Returns the earliest Date in the Document.
        # Format = dd.mm.yy

        Dates = list()
        for Token in allTokens:
            DateValue = re.search('\d{2}\.\d{2}\.\d{2}', Token)
            if DateValue is not None:
                try:
                    Dates.append(datetime.strptime(DateValue.string[:8], '%d.%m.%y'))
                except:
                    pass
        if Dates:
            return max(Dates)
        return None

    def findLatestDateTimeBouthFormats(self, allTokens):
        FullYear = self.findLatesDateTimeFullYear(allTokens)
        ShortYear = self.findEndDateTimeShortYear(allTokens)
        if (FullYear is not None) and (ShortYear is not None):
            return max(FullYear, ShortYear)
        elif (FullYear is not None):
            return FullYear
        elif (ShortYear is not None):
            return ShortYear
        return None

    def findLatesDateTimeFullYear(self, allTokens):

        # Returns the earliest Date in the Document.
        # Format = dd.mm.yyyy

        Dates = list()
        for Token in allTokens:
            DateValue = re.search('\d{2}\.\d{2}\.\d{4}', Token)
            if DateValue is not None:
                try:
                    Dates.append(datetime.strptime(DateValue.string[:10], '%d.%m.%Y'))
                except:
                    pass
        if Dates:
            return max(Dates)
        return None

    def findLatesTime(self, allTokens):
        dates = list()

        for Token in allTokens:
            DateValue = re.search('\d{2}:\d{2}:\d{2}', Token)
            if DateValue is not None:
                try:
                    dates.append(datetime.strptime(DateValue.string, "%H:%M:%S"))
                except:
                    pass

        if dates:
            return max(dates)
        return None
