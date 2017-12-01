from .utils import upper

def Monguo(_,o):
    definition = _.definitions['Monguo']
    out = '\n'.join([
        "\'''",
        _._header(o),
        "\'''\n",
        definition['imports'],
        definition['document'].format(name=o.name)
    ])

    for x in _._getmembers(o): # write members
        name = x[0]
        f = x[1][0]
        req = x[1][1]
        isList = x[1][2]
        fieldType = upper(f[0]) + f[1:]

        req = 'required=True' if req else ''

        if isList :
            if f in _.classes:
                field = "ListField(ReferenceField('%s'),%s)" % (fieldType,req)
            else:
                field = "ListField(%sField(),%s)" % (fieldType,req)

        else :
            if f in _.classes:
                field = "ReferenceField('%s',%s)" % (fieldType,req)
            else:
                field = "%sField(%s)" % (fieldType,req)


        f = "%s = %s" % (name,field)

        out += '    ' + f + '\n'

    if o.cat.checkState():
        out += 2*'\n' + definition['makeCategory'].format(o.name)

    _._write(out,o.name,definition['file'].format(o.name))
    return out
