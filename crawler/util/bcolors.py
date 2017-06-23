class Bcolors:
    """ colorize the output """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    @staticmethod
    def OKBLUEFUNC(message):
        return Bcolors.OKBLUE + message + Bcolors.ENDC

    @staticmethod
    def OKGREENFUNC(message):
        return Bcolors.OKGREEN + message + Bcolors.ENDC

    @staticmethod
    def FAILFUNC(message):
        return Bcolors.FAIL + message + Bcolors.ENDC

    @staticmethod
    def WARNINGFUNC(message):
        return Bcolors.WARNING + message + Bcolors.ENDC