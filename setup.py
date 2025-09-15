import setuptools

with open("README.md") as f:
	long_description = f.read()

setuptools.setup(
	name = "wharfy",
	packages = setuptools.find_packages(),
	version = "0.0.2",
	license = "gpl-3.0",
	description = "Tiny Docker orchestration toolkit without Yaml",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Johannes Bauer",
	author_email = "joe@johannes-bauer.com",
	url = "https://github.com/johndoe31415/wharfy",
	download_url = "https://github.com/johndoe31415/wharfy/archive/v0.0.2.tar.gz",
	keywords = [ "docker", "orchestration" ],
	install_requires = [ ],
	entry_points = {
		"console_scripts": [
			"wharfy = wharfy.__main__:main"
		]
	},
	include_package_data = False,
	classifiers = [
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.12",
		"Programming Language :: Python :: 3.13",
	],
)
