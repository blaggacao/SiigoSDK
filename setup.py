#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='siigo',
    version='1.0.0',
    author='Preki',
    author_email='david@preki.com',
    packages=['siigo', 'siigo.models', 'siigo.utils'],
    url='https://preki.com',
    download_url='https://github.com/GoPreki/SiigoSDK',
    license='MIT',
    description='Python library for handling Siigo integration',
    long_description='Python library for handling Siigo integration',
    install_requires=[
        'requests==2.27.0',
    ],
)
