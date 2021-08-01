import setuptools

with open ("README.md", "r") as infile:
    long_description = infile.read()

setuptools.setup(
    name = "autobuffer",
    version = "0.0.3",
    author = "João Dias Carrilho",
    description = "A simple and fast automatic double buffer class for 1-D data streaming",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url="https://github.com/jadc197/autobuffer",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.8',                # Minimum version requirement of the package
    py_modules=["autobuffer"],             # Name of the python package
    package_dir={'':'src/autobuffer'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)
