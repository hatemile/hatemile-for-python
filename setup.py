# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module to setup HaTeMiLe for Python.
"""

from setuptools import find_packages
from setuptools import setup

setup(
    name='hatemile',
    description=(
        'HaTeMiLe is a library that can convert a HTML code in a HTML code '
        + 'more accessible.'
    ),
    long_description=(
        'HaTeMiLe (HTML Accessible) is a open source library developed to '
        + 'improve accessibility converting a HTML code in a new HTML code '
        + 'more accessible, its features is based in WCAG 2.0 document, eMAG '
        + '3.1 document and some features of Job Access With Speech (JAWS), '
        + 'Opera before version 15 and Mozilla Firefox.\n\n'
        + 'HaTeMiLe objectives:\n\n'
        + '* Improve the accessibility of pages, avoiding create new '
        + 'inaccessibility problems;\n'
        + '* Not change the original visual of converted pages;\n'
        + '* Not change the features of original pages;\n'
        + '* Allow that users and developers can use the HaTeMiLe features;\n'
        + '* Allow that users and developers can change the texts of library;'
        + '\n'
        + '* Allow that the library can be used, extended and changed for any '
        + 'people.'
    ),
    version='2.0.0',
    url='https://github.com/hatemile/hatemile-for-python',
    author='Carlson Santana Cruz',
    license='Apache2',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries'
    ],
    packages=[
        '',
        'js',
        '_locales',
        '_locales.en_US'
    ] + find_packages(),
    package_data={
        '': ['*.xml'],
        'js': ['*'],
        '_locales': ['*'],
        '_locales.en_US': ['*']
    },
    install_requires=[
        'alabaster>=0.7.10',
        'astroid>=1.6.5',
        'Babel>=2.6.0',
        'beautifulsoup4>=4.6.0',
        'certifi>=2018.4.16',
        'chardet>=3.0.4',
        'docutils>=0.14',
        'idna>=2.6',
        'imagesize>=1.0.0',
        'isort>=4.3.4',
        'Jinja2>=2.10',
        'lazy-object-proxy>=1.3.1',
        'MarkupSafe>=1.0',
        'mccabe>=0.6.1',
        'packaging>=17.1',
        'pycodestyle>=2.4.0',
        'Pygments>=2.2.0',
        'pylint>=1.9.2',
        'pyparsing>=2.2.0',
        'pytz>=2018.4',
        'requests>=2.18.4',
        'six>=1.11.0',
        'snowballstemmer>=1.2.1',
        'Sphinx>=1.7.5',
        'sphinxcontrib-websupport>=1.1.0',
        'tinycss>=0.4',
        'urllib3>=1.22',
        'wrapt>=1.10.11'
    ]
)
