import setuptools

setuptools.setup(
    name="feathery-server-sdk",
    version="0.0.3",
    author="Markie Wagner, Peter Dun",
    author_email="me@markiewagner.com",
    description="Server-Side Python SDK for Feathery.",
    url="https://github.com/feathery-org/feathery-python-server-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
