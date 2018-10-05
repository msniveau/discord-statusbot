import os.path, configparser
from bin import __bundledir__
from shutil import copyfile
from lib.util.error import ConfigurationError
from lib.util.config import config
from os.path import expanduser

class parameter():
    __instance = None

    @staticmethod
    def getInstance():
        return parameter.__instance

    def __init__(self, parser):
        self.parser = parser
        self.parser.add_argument('--config', dest='config', help='Defines the config path (default: ~/config.ini)')
        self.parser.add_argument('--token', dest='token', help='Discord token')
        self.parser.add_argument('--monitoring-interval', dest='monitoring_interval', help='Interval of the monitoring in seconds (default: 60)')
        self.parser.add_argument('--dsn', dest='dsn', help='Sentry DSN for error logging')
        self.parser.add_argument('-v', action='store_true', dest='verbose', help='Print every message the bot is receiving (debug only)')
        self.parser.add_argument('-vv', action='store_true', dest='verbose_extended', help='More detailed version of -v')
        self.args=parser.parse_args()
        self.__config__ = config.getInstance(self.getConfig())
        parameter.__instance = self

    def getConfig(self):
        if self.args.config == None:
            config = expanduser('~') + '/config.ini'
        else:
            config=self.args.config
        if not os.path.isfile(config):
            if self.isDebugMode():
                print('[info  ] Config file not found, creating it.')
            copyfile(__bundledir__ + '/config.ini.dist', config)
        return config

    def getToken(self):
        if not self.args.token:
            if os.path.isfile(self.getConfig()):
                try:
                    return self.__config__.get('discord', 'token')
                except configparser.NoSectionError:
                    raise ConfigurationError('Unable to get discord token')
            else:
                raise AttributeError("Config file not found")
        return self.args.token

    def getDSN(self):
        if not self.args.dsn:
            if os.path.isfile(self.getConfig()):
                try:
                    dsn = self.__config__.get('sentry', 'dsn')
                    if len(dsn.strip()) > 0:
                        return dsn
                except configparser.NoSectionError:
                    return False
                return False
            else:
                raise AttributeError("Config file not found")
        return self.args.dsn

    def getMonitoringInterval(self):
        if not self.args.monitoring_interval:
            return 60
        return self.args.monitoring_interval

    def isVerbose(self):
        return self.args.verbose != False or self.args.verbose_extended != False

    def isDebugMode(self):
        return self.args.verbose_extended != False

    def printHelp(self):
        self.parser.print_help()