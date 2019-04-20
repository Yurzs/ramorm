import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="ramorm",
    version="0.0.11",
    author="Yurzs",
    description="Model based ORM in RAM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yurzs/ramorm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
)