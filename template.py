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
    return template.render(structs=ast['structs'], config=ast['config'])

