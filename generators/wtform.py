from .utils import upper

def WtForm(_,o):
    # retrieve class template
    definition = _.definitions['WtForm']
    imports = definition['imports']
    Cls = definition['class']
    # generate head
    # generate class with head

    fields = []

    for x in _._getmembers(o): # write members

        name = x[0]
        f = upper(x[1][0])
        fieldType = upper(f[0]) + f[1:]

        req = x[1][1]
        isList = x[1][2]
        validators = 'validators=[InputRequired()]' if req else ''

        '''
        if f not in _.classes and f not in fieldsImported and f != 'Oid':
            fieldsImported.append(fieldType + 'Field')
        '''
        if isList :
            if f in _.classes:
                field = "ListField(OidField(),%s)" % (validators)
            else:
                field = "ListField(%sField(),%s)" % (fieldType,validators)

        else :
            if f in _.classes:
                field = "OidField()" # required
            else:
                field = "%sField(%s)" % (fieldType,validators)

        fields.append("    %s = %s" % (name,field))


    #importFields = 'from wtforms.fields import (%s)' % ','.join(fieldsImported)

    out = '\n'.join([ imports, Cls.format(name=o.name+'CreateForm') ])
    out += '\n'.join(fields)
    out += '\n' + Cls.format(name=o.name+'UpdateForm')
    out += '\n'.join(fields)
    out += '\n' + Cls.format(name=o.name+'DeleteForm') + '    _id = ListField(OidField())' + '\n'

    _._write(out,o.name,definition['file'].format(o.name))
    return out
