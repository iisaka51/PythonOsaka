from jinja2 import FileSystemLoader, Environment

def double(arg):
    data=''
    for s in list(str(arg)):
        data += s*2
    return data

def render_from_template(directory, template_name, **kwargs):
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    env.filters['double'] = double
    template = env.get_template(template_name)
    return template.render(kwargs)

items=['Osaka', 'Python', '<Jinja2>']
numbers=[n for n in range(10)]

doc = render_from_template('.', 'filter_example.html',
                           items=items, numbers=numbers)
print(doc)
