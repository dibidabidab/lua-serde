# Files
from os import path

import yaml
import math


def readMultiAST(paths, includeHeader):
    return [readAST(path.replace('\\', '/'), includeHeader) for path in paths]


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

def mustExist(dict, key, default):
    if not key in dict:
        dict[key] = default

def moveFlags(key, struct):
    splitted = key.split('@')

    for flag in splitted[1:]:
        if not "_flags" in struct:
            struct["_flags"] = []
        struct["_flags"].append(flag.strip())

    return splitted[0].strip()


def prepareAST(full, basepath, includeHeader):
    config = popOr(full, 'config', {})
    structs = {}
    for key in full:
        structName = moveFlags(key, full[key])
        print("      " + structName)
        structs[structName] = prepareStruct(full[key])
    config['pragma_once'] = basepath.replace('.', '_').replace('/', '_').replace('\\', '_')
    mustExist(config, 'fwd_decl', [])
    mustExist(config, 'cpp_incl', [])
    mustExist(config, 'hpp_incl', [])
    config["hpp_incl"].append(includeHeader)

    return {
        'config': config,
        'structs': structs,
        'filename': path.basename(basepath),
    }


def prepareStruct(struct):
    if struct is None or type(struct) is str:
        struct = {}

    cpp_only = popOr(struct, '_cpp_only', {})
    methods = popOr(struct, '_methods', [])
    hash = popOr(struct, '_hash', None)
    flags = popOr(struct, '_flags', [])

    nr_of_vars = len(struct) + len(cpp_only)
    dirty_flags_type = "uint"
    if nr_of_vars > 8:
        dirty_flags_type += str(2**(math.ceil(math.log(nr_of_vars, 2))))
    else:
        dirty_flags_type += "8"

    return {
        'flags': flagDict(flags),
        'expose': prepareVars(struct),
        'cpp_only': prepareVars(cpp_only),
        'methods': methods,
        'hash': hash,
        'dirty_flags_type': dirty_flags_type
    }


def flagDict(flags):
    dict = {
        'json_with_keys': False,
        'not_a_component': False,
        'dirtyable': False,
    }

    for flag in flags:
        if not flag in dict:
            raise Exception('Invalid flag: ' + flag)
        dict[flag] = True

    return dict


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
