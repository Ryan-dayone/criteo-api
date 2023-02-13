"""

Author: Ryan Morlando
Created: 
Updated: 
V1.0.0
Patch Notes:

To Do:

"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='criteo-api',
    version='1.0.1',
    author='Ryan Morlando',
    author_email='ryan@dayonedigital.com',
    description='Criteo API access',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Ryan-dayone/criteo-api',
    license='MIT',
    packages=['criteo_api'],
    install_requires=['requests', 'pandas'],
)
