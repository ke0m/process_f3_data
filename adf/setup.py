from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
import subprocess
import site

VERSION = '0.0.1'
DESCRIPTION = """A package for adaptive multidimentional non-stationary
                 filtering"""
LONG_DESCRIPTION = """A package for adaptive multidimensional non-stationary
                      filtering of images and data.  Includes stationary
                      and non-stationary PEFs, and debubble"""


class Build(build_py):
  """Custom build for building PyBind11 modules"""

  def run(self):
    cmd = "cd ./adf/stat/src && make INSTALL_DIR=%s" % (
        site.getsitepackages()[0])
    subprocess.check_call(cmd, shell=True)
    cmd = "cd ./adf/nstat/src && make INSTALL_DIR=%s" % (
        site.getsitepackages()[0])
    subprocess.check_call(cmd, shell=True)
    build_py.run(self)


class Develop(develop):
  """Custom build for building PyBind11 modules in development mode"""

  def run(self):
    cmd = "cd ./adf/stat/src && make"
    subprocess.check_call(cmd, shell=True)
    cmd = "cd ./adf/nstat/src && make"
    subprocess.check_call(cmd, shell=True)
    develop.run(self)


# Setting up
setup(
    name="adf",
    version=VERSION,
    author="Joseph Jennings",
    author_email="<joseph29@sep.stanford.edu>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    cmdclass={
        'build_py': Build,
        'develop': Develop,
    },
    keywords=['seismic', 'signal', 'image', 'processing'],
    classifiers=[
        "Intended Audience :: Seismic processing/imaging",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux ",
    ],
)
