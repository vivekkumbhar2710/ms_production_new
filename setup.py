from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ms_production/__init__.py
from ms_production import __version__ as version

setup(
	name="ms_production",
	version=version,
	description="Machine Shop Production",
	author="Abhishek Chougule",
	author_email="chouguleabhis@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
