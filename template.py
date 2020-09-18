# Rendering
from jinja2 import Environment, FileSystemLoader
import pathlib

env = Environment(
    loader=FileSystemLoader(pathlib.Path(__file__).parent.absolute().__str__() + '/templates'),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

template = env.get_template('struct.jinja')


def renderStructs(ast):
    genStringTrees(ast)
    return template.render(structs=ast['structs'], config=ast['config'])


def genStringTrees(ast):
    for struct in ast['structs'].values():
        struct['split'] = stringTree(struct['expose'])


class Bucket:
    def __init__(self, mode, index):
        self.mode = mode
        self.index = index
        self.buckets = {}

    def insert(self, key, value):
        if key not in self.buckets:
            self.buckets[key] = []
        self.buckets[key].append(value)

    def singleton(self):
        return len(self.buckets) < 2

    def mbsize(self):
        return max([len(sbucket) for sbucket in self.buckets.values()])


def stringTree(fields, key=None):
    if len(fields) == 0:
        return {'mode': 'empty'}
    if len(fields) == 1:
        return {'mode': 'singleton', 'key': key, 'value': fields[0]}

    splits = []
    letterSplits(fields, splits)
    lengthSplits(fields, splits)

    minSplit = min(splits, key=lambda bucket: bucket.mbsize())

    return {
        'mode': minSplit.mode,
        'index': minSplit.index,
        'key': key,
        'buckets': [stringTree(bucket, key) for key, bucket in minSplit.buckets.items()],
    }


def letterSplits(fields, splits):
    length = min([len(value.name) for value in fields])
    for i in range(length):
        bucket = Bucket('letter', i)
        for field in fields:
            bucket.insert("'" + field.name[i] + "'", field)
        if not bucket.singleton():
            splits.append(bucket)


def lengthSplits(fields, splits):
    bucket = Bucket('length', 0)
    for field in fields:
        bucket.insert(len(field.name), field)
    if not bucket.singleton():
        splits.append(bucket)
