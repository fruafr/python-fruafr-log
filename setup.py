#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup dot py."""
from __future__ import absolute_import, print_function

# import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read description files."""
    path = join(dirname(__file__), *names)
    with open(path, encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()

# previous approach used to ignored badges in PyPI long description
# long_description = '{}\n{}'.format(
#     re.compile(
#         '^.. start-badges.*^.. end-badges',
#         re.M | re.S,
#         ).sub(
#             '',
#             read('README.rst'),
#             ),
#     re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read(join('docs', 'CHANGELOG.rst')))
#     )

long_description = '{}\n{}'.format(
    read('README.md'),
    read('CHANGELOG.md'),
    )

setup(
    name='fruafr.log',
    version='0.0.1',
    description='Simple logging library based on the standard Python logging',
    long_description=long_description,
    long_description_content_type='text/x-md',
    license='Apache-2.0',
    author='David HEURTEVENT',
    author_email='david@heurtevent.org',
    url='https://github.com/fruafr/python-fruafr-log',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(i))[0] for i in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        # 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console'
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.10',
        'Topic :: System :: Logging',
        ],
    project_urls={
        'webpage': 'ttps://github.com/fruafr/python-fruafr-log',
        #'Documentation': 'https://python-project-skeleton.readthedocs.io/en/latest/',
        'Changelog': 'ttps://github.com/fruafr/python-fruafr-log/blob/master/CHANGELOG.rst',
        'Issue Tracker': 'ttps://github.com/fruafr/python-fruafr-log/issues',
        'Discussion Forum': 'https://github.com/fruafr/python-fruafr-log/discussions',
        },
    keywords=[
        'logging', 'cli', 'console logging', 'file logging',
        # eg: 'keyword1', 'keyword2', 'keyword3',
        ],
    python_requires='>=3.10, <4',
    install_requires=[
        # https://stackoverflow.com/questions/14399534
        #'matplotlib>=3',
        ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
        },
    setup_requires=[
        #   'pytest-runner',
        #   'setuptools_scm>=3.3.1',
        ],
    entry_points={
        #'console_scripts': [
        #    'samplecli1= sampleproject.cli_int1:main',
        #    ]
        #
        },
    # cmdclass={'build_ext': optional_build_ext},
    # ext_modules=[
    #    Extension(
    #        splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
    #        sources=[path],
    #        include_dirs=[dirname(path)]
    #    )
    #    for root, _, _ in os.walk('src')
    #    for path in glob(join(root, '*.c'))
    # ],
    )
