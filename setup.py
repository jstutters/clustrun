import codecs
import os.path
from setuptools import find_packages, setup

project = 'snakerunner'
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name=project,
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=True,
    author='Jon Stutters',
    author_email='j.stutters@ucl.ac.uk',
    description='A tool for distributing tasks across a range of servers using SSH',
    long_description=long_description,
    url='https://hydra.nmr.ion.ucl.ac.uk/jstutters/snakerunner',
    install_requires=[
        'click',
        'fabric',
    ],
    setup_requires=[],
    tests_require=[],
    entry_points={
        'console_scripts': ['snakerunner=snakerunner.main:run']
    },
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Logging'
    ]
)