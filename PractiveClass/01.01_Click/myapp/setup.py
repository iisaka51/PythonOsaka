from setuptools import setup

setup(
    name='myapp',
    version='0.1',
    py_modules=['myapp'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        myapp=click_myapp:cli
    ''',
)
