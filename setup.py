from setuptools import setup
import os

VERSION = "0.1a1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="sphinx-to-sqlite",
    description="Create a SQLite database from Sphinx documentation",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/sphinx-to-sqlite",
    project_urls={
        "Issues": "https://github.com/simonw/sphinx-to-sqlite/issues",
        "CI": "https://github.com/simonw/sphinx-to-sqlite/actions",
        "Changelog": "https://github.com/simonw/sphinx-to-sqlite/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["sphinx_to_sqlite"],
    entry_points="""
        [console_scripts]
        sphinx-to-sqlite=sphinx_to_sqlite.cli:cli
    """,
    install_requires=["click", "sqlite-utils"],
    extras_require={"test": ["pytest"]},
    tests_require=["sphinx-to-sqlite[test]"],
)
