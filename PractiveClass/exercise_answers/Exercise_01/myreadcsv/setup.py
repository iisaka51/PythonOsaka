from setuptools import setup
import myreadcsv

setup(
    name='myreadcsv',
    version=myreadcsv.__version__,
    py_modules=['myreadcsv'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        myreadcsv=myreadcsv:readcsv
    ''',
)
