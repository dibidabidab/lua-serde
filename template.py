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
    return template.render(structs=ast['structs'], config=ast['config'])


class Bucket:
    mode = 'letter'
    index = 0
    buckets = {}

    def insert(self, key, value):
        if self.buckets[key] is None:
            self.buckets[key] = set()
        self.buckets[key].add(value)

    def singleton(self):
        return len(self.buckets) < 2

    def similar(self, other):
        mine = set([sbuck for sbuck in self.buckets.values()])
        their = set([sbuck for sbuck in other.buckets.values()])
        return mine == their


def stringTree(bucket):
    splits = []


def letterSplits(set, splits):
    length = min([len(value.name) for value in set])
    for i in range(length):
        bucket = Bucket()
        for field in set:
            bucket.insert(field.name[i], field)
        addIfGood(bucket, splits)


def lengthSplits(set, splits):
    for pivot in set:
        bucket = Bucket()
        for field in set:
            key = 'l' if len(field.name) <= len(pivot.name) else 'h'
            bucket.insert(key, field)
        addIfGood(bucket, splits)


def addIfGood(bucket, splits):
    good = True
    if bucket.singleton():
        good = False
    for split in splits:
        if split.similar(bucket):
            good = False
    if good:
        splits.append(bucket)
