
from setuptools import setup, find_packages
from ubw.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='ubw',
    version=VERSION,
    description='The meta tool for RT-Thread',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='wugensheng',
    author_email='shinu_61@163.com',
    url='https://github.com/wugensheng-code/ubw',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'ubw': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        ubw = ubw.main:main
    """,
)
