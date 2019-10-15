# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['listdict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'listdict',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Aaron Christianson',
    'author_email': 'ninjaaron@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
