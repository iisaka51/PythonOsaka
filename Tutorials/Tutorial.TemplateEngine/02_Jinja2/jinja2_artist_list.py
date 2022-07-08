from jinja2 import FileSystemLoader, Environment

def render_from_template(directory, template_name, **kwargs):
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(kwargs)

class Artist:
    pass

artist_list=[
    {
        'firstname': 'Freddie',
        'lastname': 'Mercury',
        'born_place': 'Farrokh Bulsara',
        'born_date': '1946-9-5'
    },
    {
        'firstname': 'David',
        'lastname': 'Bowie',
        'born_place': 'Brixton, London, England',
        'born_date': '1947-1-8'
    },
]

doc = render_from_template('.', 'artist_list.html', artist_list=artist_list)
print(doc)
