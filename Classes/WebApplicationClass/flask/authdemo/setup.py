from setuptools import setup

setup(
    name='authdemo',
    version='0.1',
    py_modules=['app'],
    install_requires=[
        'flask',
        'flask-migrate',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-wtf',
        'Click',
        'jinja2',
    ],
    entry_points='''
        [console_scripts]
        authdemo=app:main
    ''',
)
