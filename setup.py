from setuptools import setup, find_packages

setup(
    name='pvr',
    version='0.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    url='',
    license='Apache License 2.0',
    author='Ben Gidley',
    author_email='ben@gidley.co.uk',
    description='Prepare content recorded off DTV',
    install_requires=['av'],
    entry_points={
        'console_scripts': [
            'pvr=pvr.pvr:cli',
        ],
    },
)
