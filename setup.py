from distutils.core import setup
from setuptools import find_packages

setup(name='drawing3d',
      version='0.1',
      author='Andreas Kist',
      author_email='anki@neuro.mpg.de',
      packages=find_packages(),
      install_requires=['numpy', 'numba', 'scikit-image'])
