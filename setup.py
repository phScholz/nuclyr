from setuptools import setup, find_packages
import os
import ast
from pip import __file__ as pip_loc

def extract_values(source_file, desired_vars):
    with open(source_file) as f:
        for line in f:
            if any(line.startswith(var) for var in desired_vars):
                parsed = ast.parse(line).body[0]
                yield parsed.targets[0].id, parsed.value.s

with open("README.md", "r") as fh:
    long_description = fh.read()
  
package_name="nuclyr"

data_file_source = os.path.join(os.path.dirname(__file__), package_name)
data_install_folder = os.path.join(os.path.dirname(os.path.dirname(pip_loc)), package_name)

for filename in os.listdir(data_file_source):
  all_data_files = os.path.join(data_file_source, filename)

data_files = [(data_install_folder, all_data_files)]

setup(name='nuclyr',
      version='0.17',
      author='Philipp Scholz',
      author_email='pscholz@outlook.com',
      license='MIT',
      packages=["nuclyr"],
      package_dir={package_name: package_name},
      #data_files=[("","ripl/abundance.dat"), ("","ripl/mass-frdm95.dat"),("","./admc/mass16.dat")],
      include_package_data = True,
      url="https://github.com/phScholz/nuclyr",
      description="An utility package for nuclear data.",
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False,
      install_requires=['selenium','pandas', 'numpy', 'requests'])