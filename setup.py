# lowrapper - setup

from setuptools import setup
from os.path import exists


NAME = "lowrapper"


if exists("README.md"):
    with open("README.md", "r") as f:
        long_description = f.read()
else:
    long_description = "..."


with open(f"{NAME}/__init__.py", "r") as f:
    text = f.read()
    version = text.split('__version__ = "')[1].split('"')[0]
    author = text.split('__author__ = "')[1].split('"')[0]


setup(
    name=NAME,
    version=version,
    description='Make API wrapper in fast, easy.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f'https://github.com/tasuren/{NAME}',
    project_urls={
        "Documentation": f"https://tasuren.github.io/{NAME}/"
    },
    author=author,
    author_email='tasuren5@gmail.com',
    license='MIT',
    keywords='api wrapper',
    packages=[
        "lowrapper"
    ],
    install_requires=["requests"],
    extras_requires={
        "asynchronous": ["aiohttp"],
        "documentation": ["pdoc"]
    },
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)