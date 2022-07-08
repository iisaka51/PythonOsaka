from jinja2 import FileSystemLoader, Environment

def render_from_template(directory, template_name, **kwargs):
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(kwargs)

class Artist:
    pass

artist = Artist()
artist.firstname = 'Freddie'
artist.Lastname = 'Mercury'
artist.born_place = 'Farrokh Bulsara'
artist.born_date = '1946-9-5'

doc = render_from_template('.', 'artist.html', artist=artist)
print(doc)
