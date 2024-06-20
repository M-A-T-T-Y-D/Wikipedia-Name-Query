"""Python setup.py for wikipedia_name_query package"""
import io
import os
from setuptools import setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("wikipedia_name_query", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="wikipedia_name_query",
    version=read("wikipedia_name_query", "VERSION"),
    description="Awesome wikipedia_name_query created by M-A-T-T-Y-D",
    url="https://github.com/M-A-T-T-Y-D/Wikipedia-Name-Query/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="M-A-T-T-Y-D",
    license= 'MIT',
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["wikipedia_name_query = wikipedia_name_query.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
    zip_safe=False
    )
