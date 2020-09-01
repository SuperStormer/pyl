import setuptools
with open("README.md", "r") as f:
	long_description = f.read()
setuptools.setup(
	name="pyl",
	version="0.1",
	descripton="General purpose text processing tool",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=["pyl"],
	license="MIT",
	author="SuperStormer",
	author_email="larry.p.xue@gmail.com",
	url="https://github.com/SuperStormer/pyl",
	project_urls={"Source Code": "https://github.com/SuperStormer/pyl"},
	entry_points={"console_scripts": ["pyl=pyl.pyl:main"]},
)