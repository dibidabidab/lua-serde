# Files
from os import path
from glob import glob

import yaml


def readMultiAST(paths):
    return [readAST(path) for path in paths]


def readAST(configPath):
    file = open(configPath)
    structs = yaml.load(file, Loader=yaml.FullLoader)
    basepath, _ = path.splitext(configPath)
    return prepareAST(structs, basepath)


# Prepare for generation
def popOr(dict, key, default):
    if key in dict:
        return dict.pop(key)
    return default


def prepareAST(structs, basepath):
    config = popOr(structs, 'config', {})
    for key in structs:
        structs[key] = prepareStruct(structs[key])
    config['pragma_once'] = basepath.replace('.', '_').replace('/', '_')

    return {
        'config': config,
        'structs': structs,
        'filename': path.basename(basepath),
    }


def prepareStruct(struct):
    cpp_only = popOr(struct, '_cpp_only', {})
    methods = popOr(struct, '_methods', [])
    hash = popOr(struct, '_hash', [])

    return {
        'expose': prepareVars(struct),
        'cpp_only': prepareVars(cpp_only),
        'methods': methods,
        'hash': hash
    }


def prepareVars(dict):
    prepared = []
    for key, value in dict.items():
        if type(value) is list:
            typ, default = value
            prepared.append({
                'name': key,
                'typ': typ,
                'default': default,
            })
        else:
            prepared.append({
                'name': key,
                'typ': value,
            })
    return prepared
