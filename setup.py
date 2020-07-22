"""This file helps to publish the module."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SwaANSI-pkg-swajime",
    version="0.1.0",
    author="John Simpson",
    author_email="john@swajime.com",
    description="Enable wrapping text with color and attributes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swajime/ansi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
