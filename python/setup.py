import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="statbotics",
    version="0.0.1",
    author="Abhijit Gupta",
    author_email="avgupta456@gmail.com",
    description="Modernizing FRC Data Analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avgupta456/statbotics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
