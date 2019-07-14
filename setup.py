#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
>>> python setup.py sdist
>>> python setup.py bdist --format=zip
"""
from setuptools import setup
from setuptools import find_packages


setup(
    name='trest',
    version='1.0.0',
    description='基于Tornado结合asyncio的web mvc框架',
    author='leeyi',
    author_email='leeyisoft@icloud.com',
    url='https://gitee.com/leeyi/trest',
    license='MIT Licence',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'tornado>=6.0.0',
        'mysqlclient',
        'sqlalchemy',
        'sqlalchemy-utils',
        'redis==2.10.6',
        'requests',
        'PyJWT',
        'python-dateutil',
        'pytz',
        'rsa',
        'pycryptodome',
        'raven',
        'pika',
        'pillow',
        'qrcode',
        'oss2',
    ],
)
