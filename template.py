# Rendering
from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('templates'),
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
        struct['split'] = stringTree(set(struct['expose']))

class Bucket:
    def __init__(self, mode, index):
        self.mode = mode
        self.index = index
        self.buckets = {}

    def insert(self, key, value):
        if key not in self.buckets:
            self.buckets[key] = set()
        self.buckets[key].add(value)

    def singleton(self):
        return len(self.buckets) < 2

    def mbsize(self):
        return max([len(sbucket) for sbucket in self.buckets.values()])


def stringTree(set):
    if len(set) == 0:
        return {'mode': 'empty'}
    if len(set) == 1:
        return {'mode': 'singleton', 'value': list(set)[0]}

    splits = []
    letterSplits(set, splits)
    lengthSplits(set, splits)

    minSplit = min(splits, key=lambda bucket: bucket.mbsize())

    return {
        'mode': minSplit.mode,
        'index': minSplit.index,
        'buckets': [genSplit(key, set) for key, set in minSplit.buckets.items()],
    }


def genSplit(key, set):
    return {
        'key': key,
        'node': 'leaf' if len(set) == 1 else 'node',
        'value': list(set)[0] if len(set) == 1 else stringTree(set)
    }


def letterSplits(set, splits):
    length = min([len(value.name) for value in set])
    for i in range(length):
        bucket = Bucket('letter', i)
        for field in set:
            bucket.insert(field.name[i], field)
        if not bucket.singleton():
            splits.append(bucket)


def lengthSplits(set, splits):
    for pivot in set:
        bucket = Bucket('length', len(pivot.name))
        for field in set:
            key = '<' if len(field.name) <= len(pivot.name) else '>'
            bucket.insert(key, field)
        if not bucket.singleton():
            splits.append(bucket)
