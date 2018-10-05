from configparser import ConfigParser

class config:
    __instance = None

    @staticmethod
    def getInstance(path = None):
        if config.__instance == None:
            config(path)
        return config.__instance

    def __init__(self, path):
        if config.__instance != None:
            raise Exception("Cannot load config file again, use getInstance instead")
        else:
            config.__instance = ConfigParser()
            config.__instance.read(path)