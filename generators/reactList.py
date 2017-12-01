from .utils import upper, lower

def ReactList(_,o):

        definition = _.definitions['reactList']
        imports = definition['imports']
        th = definition['th']
        td = definition['td']
        members = [m[0] for m in _._getmembers(o)] #

        fields = {
            'name': lower(o.name),
            'Name': upper(o.name),
            'th' : '\n'.join([th.format(m) for m in members]),
            'td' : '\n'.join([td.format(m) for m in members]),
        }

        Class = definition['class'].format(**fields)
        out = "/*\n%s*/\n%s\n%s" % ( _._header(o), imports, Class)
        _._write(out,o.name,definition['file'].format(o.name))
        return out
