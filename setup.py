from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='nuclyr',
      version='0.15',
      author='Philipp Scholz',
      author_email='pscholz@outlook.com',
      license='MIT',
      packages=['nuclyr'],
      data_files=[],
      url="https://github.com/phScholz/nuclyr",
      description="An utility package for nuclear data.",
      long_description="An utility package for nuclear physics.\
        Features include the automatic data mining from the EXFOR database",
      zip_safe=False,
      install_requires=['selenium','pandas'])