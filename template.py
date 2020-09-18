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
    print(ast)
    return template.render(structs=ast['structs'], config=ast['config'])

