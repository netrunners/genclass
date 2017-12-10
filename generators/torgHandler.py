from .utils import upper, lower

def TorgHandler(_,o):
    definition = _.definitions['TorgHandler']
    urlpattern = definition['urlpattern']
    members = _._getmembers(o)
    CRUD = 'Create Read Update Delete List FullList'.split()

    docdict = '\n'.join(["%s%s%s" % (
                        3*'    ',
                        definition['member'].format(name=x[0]),
                        "," ) for x in members])

    dform = { # those use memberlist
        'Create':True,
        'Update':True
    }

    h = "\'''\n%s\n'''\n" % _._header(o)
    imports = "%s\n" % definition['imports'].format(
        name=lower(o.name),
        Name=upper(o.name))

    if o.cat.checkState():
        imports += "%s\n" % definition['import_cat'].format(
            name=lower(o.name),
            Name=upper(o.name))

    cls = ''
    for handler in CRUD :
        print(handler)
        Cls = definition[handler]
        docmembers = docdict if dform.get(handler) else ''
        # humhum, hence the presence of '''docmembers''' in every handlers
        cls += Cls.format(name=o.name,
                          docmembers=docmembers)

    urls = '\n    '.join(
        [ urlpattern.format(
            name=lower(o.name),
            crud=lower(handler),
            Crud=handler,
            Name=upper(o.name)) for handler in CRUD ])

    localimports = "from .{0}_h import {1}".format(
        upper(o.name),
        ','.join([ o.name + crud + '_H' for crud in CRUD])
    )

    urls = "%s\nurlpattern = (\n    %s\n)\n" % (localimports,urls)

    _._write(urls,o.name,"%s/%s" % (o.name,"urlmap.py"))

    out = "%s%s%s" % (h,imports,cls)
    _._write(out,o.name,definition['file'].format(o.name))
    return out
