

import importlib
import imp
from importlib import import_module
import ast, types, sys, time
from inspect import signature, getmembers, isclass, ismethod, _empty

from monguo import Field,StringField,IntegerField, ReferenceField

import torg.debuglog
log = torg.debuglog.get(__name__)

def GetSubList(obj):

    if isclass(type(obj)):
        if type(obj) is list or type(obj) is tuple:
            # set the name as the indice in the list
            # i stays as integer for holder[i] access
            members = [(i, o) for i, o in enumerate(obj)]
            return members

        else:
            try:
                members = getmembers(
                    obj, lambda x: not isinstance(x, types.ModuleType))
                # discardedFields = [ '__builtins__','__cached__','__doc__','__file__','__loader__','__name__','__package__','__spec__']
                # __dict__,__dir__,__eq__,__format__,__ge__,__getattribute__,__gt__,__hash__,__init__,__le__,__lt__,__module__,__ne__,__new__,__reduce__,__reduce_ex__,__repr__,__setattr__,__sizeof__,__str__,__subclasshook__,__weakref__
                #print(type(members))
                #[ logger.debug(x + ' ' + str(o)) for(x,o) in members]
                #[ print(x + ' ' + str(o)) for(x,o) in members]
                members = [(name, o)
                           for (name, o) in members if not name.startswith('__')
                           ]

                #members.append(('__init__', obj.__init__))

                return members
            except Exception as e:
                log.exception(e)

    return []



def generate(Obj):

    for name, o in GetSubList(Obj):
        print(name)
        if isinstance(o,Field) :
            print(name, o.required)
        if isinstance(o,StringField) :
            print(name, o.required)


["{cls}{t}".format(cls="a", t=x) for x in [1,2]]


def forms(cls, Op):
    return '''
class {cls}{Op}(Form):
    {{fields}}
'''.format(cls=cls, Op=Op)


def generateForms(Cls, meth):

    members = getmembers( Cls, lambda x: isinstance(x, Field))

    for name, o in members:
        validators = ''
        if o.required :
            validators += '''
        InputRequired(message=T("%s")),
        ''' % name+' can''t be empty'


        print('''   %s = %s(validators=[%s]) ''' % (
            name,
            o.__class__.__name__,
            validators
        ))

        if isinstance(o,Field) :
            print(name, o.required)
        if isinstance(o,StringField) :
            print(name, o.required)


    for m in meth:
        form = forms(Obj.__name__,m)




def main():
    # x = import_module("%s.%s" % (package,module))

    #x = import_module(module,package)
    fp, pathname, description = imp.find_module("torg/api/db/Debat")
    module = imp.load_module("Debat.Debat", fp, pathname, description)
    print(module)
    generate(module)



from torg.api.db.Debat import Debat

if __name__ == '__main__':

    meth = "Create Read Update Delete"
    generateForms(Debat,meth.split())
