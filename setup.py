from setuptools import setup
from fontPens import __version__

setup(
    name='fontPens',
    version=__version__,
    author='The RoboFab Developers',
    author_email='info@robofab.com',
    packages=[
        'fontPens'
    ],
    url='http://github.com/robofab-developers/fontPens',
    license='LICENSE.txt',
    description='Classes following the pen protocol for manipulating glyphs',
    long_description=open('README.rst').read(),
    install_requires=[]
)
