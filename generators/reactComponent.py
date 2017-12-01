
def ReactComponent(_,o):

    import pprint

    definition = _.definitions['reactComponent']
    imports = definition['imports']
    field = definition['input']
    typedmembers = _._getmembers(o)
    members = [m[0] for m in _._getmembers(o)] #
    indent = '    '

    print(members)

    fields = {
        'name':o.name,
        'membersdict' : ',\n'.join([ (indent + "%s:null") % m for m in members ]),
        'memberStateDict' : ',\n'.join(["{0}:this.state.{0}".format(m) for m in members ]),
        'memberslist' : ', '.join(members),
        'andmembers' : ' && '.join(members),
        'inputs' : (indent+'\n').join( [ field.format(name=m[0],type=m[1][0]) for m in typedmembers ] )
    }


    pprint.pprint(fields)
    Class = definition['class'].format(**fields)
    out = "/*\n%s*/\n%s\n%s" % ( _._header(o), imports, Class)
    _._write(out,o.name,definition['file'].format(o.name))
    return out
