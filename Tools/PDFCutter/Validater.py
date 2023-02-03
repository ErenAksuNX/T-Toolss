# Handels the validationprocess of Tokens

class Validater:
    def __init__(self):
        self.ZustellungGrund = None

        self.ZugNr3T = ['151', '152', '153', '154', '155', '156', '157', '158', '159', '160']
        self.ZugNr5T = ['351', '352', '353', '354', '355', '356', '357', '358', '359', '360', '361', '362', '363',
                        '364', '365', '366', '367', '368', '369', '370', '371', '372', '373', '374', '375']
        self.FzNr3T = ['94809442151-8', '94809442152-6', '94809442153-4', '94809442154-2', '94809442155-9', '94809442156-7',
                       '94809442157-5', '94809442158-3', '94809442159-1', '94809442160-9']
        self.FzNr5T = ['94809442351-4', '94809442352-2', '94809442353-0', '94809442354-8', '94809442355-5',
                       '94809442356-3', '94809442357-1', '94809442358-9', '94809442359-7', '94809442360-5',
                       '94809442361-3', '94809442362-1', '94809442363-9', '94809442364-7', '94809442365-4',
                       '94809442366-2', '94809442367-0', '94809442368-8', '94809442369-6', '94809442370-4',
                       '94809442371-2', '94809442372-0', '94809442373-8', '94809442374-6', '94809442375-3']
        self.FzNr3TMed = ['9442151-8', '9442152-6', '9442153-4', '9442154-2', '9442155-9', '9442156-7', '9442157-5', '9442158-3',
                          '9442159-1', '9442160-9']
        self.FzNr5TMed = ['9442351-4', '9442352-2', '9442353-0', '9442354-8', '9442355-5', '9442356-3', '9442357-1',
                          '9442358-9', '9442359-7', '9442360-5', '9442361-3', '9442362-1', '9442363-9', '9442364-7',
                          '9442365-4', '9442366-2', '9442367-0', '9442368-8', '9442369-6', '9442370-4', '9442371-2',
                          '9442372-0', '9442373-8', '9442374-6', '9442375-3']
        self.FzNr3TShort = ['151-8', '152-6', '153-4', '154-2', '155-9', '156-7', '157-5', '158-3', '159-1', '160-9']
        self.FzNr5TShort = ['351-4', '352-2', '353-0', '354-8', '355-5', '356-3', '357-1', '358-9', '359-7', '360-5',
                            '361-3', '362-1', '363-9', '364-7', '365-4', '366-2', '367-0', '368-8', '369-6', '370-4',
                            '371-2', '372-0', '373-8', '374-6', '375-3']

    def is3TNr(self, Token):
        if Token in self.ZugNr3T:
            return True
        return False

    def is5TNr(self, Token):
        if Token in self.ZugNr5T:
            return True
        return False

    def isZugNr(self, Token):
        if Token in self.ZugNr3T or Token in self.ZugNr5T:
            return True
        return False

    def isFazNr(self, Token):
        if Token in self.FzNr3T or Token in self.FzNr5T:
            return True
        return False

    def isZustellungsGrund(self, Token):
        if Token in self.ZustellungGrund:
            return True
        return False

    def returnPossibleRepairReasons(self, multipleTokens):
        return set(self.ZustellungGrund).intersection(multipleTokens)

    def getZugNummer(self, multipleTokens):

        # Search the short FahrzeugNr
        for idx, FzNr in enumerate(self.FzNr3T):
            if FzNr in multipleTokens:
                return self.FzNr3T[idx]
        for idx, FzNr in enumerate(self.FzNr5T):
            if FzNr in multipleTokens:
                return self.FzNr5T[idx]

    def getZugNummershort(self, multipleTokens):

        # Search the short ZugNr

        for idx, FzNr in enumerate(self.ZugNr3T):
            if FzNr in multipleTokens:
                return self.ZugNr3T[idx]
        for idx, FzNr in enumerate(self.ZugNr5T):
            if FzNr in multipleTokens:
                return self.ZugNr5T[idx]

    def getZugNummerMedium(self, multipleTokens):

        # Search the short ZugNr

        for idx, FzNr in enumerate(self.FzNr3TMed):
            if FzNr in multipleTokens:
                return self.ZugNr3T[idx]
        for idx, FzNr in enumerate(self.FzNr5TMed):
            if FzNr in multipleTokens:
                return self.ZugNr5T[idx]

    def getFzNummerShort(self, multipleTokens):

        # Search the short ZugNr

        for idx, FzNr in enumerate(self.FzNr3TShort):
            if FzNr in multipleTokens:
                return self.ZugNr3T[idx]
        for idx, FzNr in enumerate(self.FzNr5TShort):
            if FzNr in multipleTokens:
                return self.ZugNr5T[idx]

    def getShortZugNummer(self, multipleTokens):

        # This Function Returns the SHort ZugNr even if there is just the long one inside the Doc.

        ZurNr = self.getZugNummer(multipleTokens)
        if ZurNr is not None:
            firstZugNr = ZurNr.partition("-")[0]
            lenFirst = len(firstZugNr)
            shortNr = firstZugNr[lenFirst - 3:]
        else:
            shortNr = self.getZugNummershort(multipleTokens)
        if shortNr == None:
            shortNr = self.getZugNummerMedium(multipleTokens)
        return shortNr

    def lowercastTokens(self, multipleTokens):
        # Returns a List with Token which are all lowerCasted
        lowerTokens = list()
        for token in multipleTokens:
            lowerTokens.append(token.lower())
        return lowerTokens

    def isPageNameNotDefined(self, filename):

        # Returns True if the Page ame belongs to a not defined Page

        if (('Freigabedokument' in filename) or
                ('SonstigeDokumente' in filename) or
                ('Arbeitsschein' in filename) or
                ('UFDProtokoll' in filename)):
            ('PZB')
            return True
        return False
