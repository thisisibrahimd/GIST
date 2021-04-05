from setuptools import setup

setup(
    name='gist',
    version='0.1',
    py_modules=['gist'],
    install_requires=[
        'click',
        'sqlalchemy',
        'sklearn',
        'python-dotenv',
        'numpy',
    ],
    entry_points='''
        [console_scripts]
        gist=gist.cli:cli
    ''',
)
