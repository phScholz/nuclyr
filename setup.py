from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='nuclyr',
      version='0.01',
      author='Philipp Scholz',
      author_email='pscholz@outlook.com',
      license='MIT',
      packages=['nuclyr'],
      url="https://github.com/phScholz/nuclyr",
      description="A utility package for nuclear data.",
      zip_safe=False)