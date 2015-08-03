"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name='pkaaw',

    version='0.0.1',

    description='Python Khan Academy API Wrapper',
    long_description='Python wrapper for the Khan Academy API, using most current auth flow.',

    url='https://github.com/almartin82/pkaaw',

    author='Andrew Martin',
    author_email='almartin@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Education'

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],

    keywords='api education khan',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['requests-oauthlib', 'requests', 'PyYAML', 'six'],

    # Entry points for command line integration
    entry_points="",

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)