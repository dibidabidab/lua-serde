# Files
from os import path

import yaml


def readMultiAST(paths, includeHeader):
    return [readAST(path, includeHeader) for path in paths]


def readAST(configPath, includeHeader):
    print("File: " + configPath)
    file = open(configPath)
    structs = yaml.load(file, Loader=yaml.FullLoader)
    basepath, _ = path.splitext(configPath)
    return prepareAST(structs, basepath, includeHeader)


# Prepare for generation
def popOr(dict, key, default):
    if key in dict:
        return dict.pop(key)
    return default


def prepareAST(structs, basepath, includeHeader):
    config = popOr(structs, 'config', {})
    for key in structs:
        print("      " + key)
        structs[key] = prepareStruct(structs[key])
    config['pragma_once'] = basepath.replace('.', '_').replace('/', '_')
    config['include_header'] = includeHeader

    return {
        'config': config,
        'structs': structs,
        'filename': path.basename(basepath),
    }


def prepareStruct(struct):
    if struct is None or type(struct) is str:
        return {
            'expose': {},
            'cpp_only': {},
            'methods': [],
            'hash': None,
        }

    cpp_only = popOr(struct, '_cpp_only', {})
    methods = popOr(struct, '_methods', [])
    hash = popOr(struct, '_hash', None)
    flags = popOr(struct, '_flags', [])

    return {
        'flags': flagDict(flags),
        'expose': prepareVars(struct),
        'cpp_only': prepareVars(cpp_only),
        'methods': methods,
        'hash': hash
    }


def flagDict(flags):
    dict = {
        'json_with_keys': False,
        'not_a_component': False,
    }

    for flag in flags:
        if not flag in dict:
            raise Exception('Invalid flag: ' + flag)
        dict[flag] = True


class Field:
    def __init__(self, name, typ, default=None):
        self.name = name
        self.typ = typ
        self.default = default

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return "Field {{name: '{}', typ: '{}', default: '{}'}}".format(self.name, self.typ, self.default)


def prepareVars(dict):
    prepared = []
    for key, value in dict.items():
        if type(value) is list:
            typ, default = value
            prepared.append(
                Field(key, fixTyp(typ), fixDefault(typ, default)))
        else:
            prepared.append(
                Field(key, fixTyp(value)))
    return prepared


def fixDefault(typ, str):
    if typ == "string":
        return '"{}"'.format(str)
    if str is False:
        return 'false'
    if str is True:
        return 'true'
    if str is None:
        return 'NULL'
    return str


def fixTyp(typ):
    if typ == "string":
        return 'std::string'
    return typ
