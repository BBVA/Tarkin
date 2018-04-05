"""
Copyright 2018 Banco Bilbao Vizcaya Argentaria, S.A.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from distutils.core import setup
import os

from setuptools import find_packages


with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name='tarkin',
    version='0.0.2',
    install_requires=required,
    packages=find_packages(),
    include_package_data=True,
    description='Fear-based detection of Security Anomalies in Log Data',
    url='https://github.com/BBVA/Tarkin',
    keywords=["Anomalies", "Logs", "Security", "AI", "Sentiment", "Fear", "Rooted"],
    license='Apache 2.0 License',
    author='Daniel Hernández León (@deccar), Cesar Gallego Rodríguez (@CesarGallegoR)',
    author_email='Cesar Gallego <cesar.gallego@bbva.com>, Daniel Hernández <daniel.hleon@bbva.com>',
)
