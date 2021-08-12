# setup file for python code installation
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="quantML",
    version="0.0.1",
    author="Clay Elmore",
    author_email="celmore25@gmail.com",
    description="library for quantitative analysis of stocks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/celmore25/",
    packages=["quantML"],
    python_requires=">=3.6",
    include_package_data=True,
)
