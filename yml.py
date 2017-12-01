import yaml


def load(file):

    class Struct:
        def __init__(self,rawdat) :
            self.__dict__ = rawdat

    with open(file) as f:
        rawDic = yaml.safe_load(f)

    return Struct(rawDic)
