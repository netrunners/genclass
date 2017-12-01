import yaml,os
from generators.utils import lower
from PyQt5.QtWidgets import QMessageBox


class Generators:
    '''
    The code generators
    the Generators are functions in this class not starting with a _
    (ie considered private in some conventions)
    '''

    def __init__(_,definitions):
        _.definitions = definitions.classes

    def _load(gens):
        for g in gens:
            setattr(Generators,g.__name__,g)

    def _classdict(_):
        return _.__class__.__dict__

    def _availables(_) :
        L = [ x for x in _._classdict() if x[0] is not '_' ]
        L.sort(reverse=False)
        implemented = L
        '''
        definitions = set(_.definitions.keys())
        ind = implemented.difference(definitions)
        dni = definitions.difference(implemented)

        if ind :
            print(ind, "an implemention exists but no template")
        if dni :
            print(dni, "template exists but not implemented ")
        '''
        return implemented


    def _write(_,content,d,f):
        dirName = lower(d)
        fileName = lower(f)
        gdir = os.path.join(_.dir,dirName)
        print(gdir,dirName,fileName)
        try:
            if not os.path.exists(gdir):
                os.mkdir(gdir)
            with open(os.path.join(_.dir,fileName),'w') as file:
                file.write(content)
        except FileNotFoundError as fnfe:
            QMessageBox.critical(None,'woops',str(fnfe), QMessageBox.Ok)

    def _get(_,x):
        return _._classdict()[x]

    def _header(_,o):
        return _.definitions['_header'].format(name=o.name)

    def _Yaml(_,o):
        return yaml.dump({
            o.name : o.members.dict()
        })

    def _getmembers(_,o):
        return [ list(x.items())[0] for x in o.members.dict() ]


