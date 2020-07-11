import setuptools

setuptools.setup(
    name="feathery-server-sdk", # Replace with your own username
    version="0.0.1",
    author="Markie Wagner, Peter Dun",
    author_email="me@markiewagner.com",
    description="A Python SDK for Feathery.",
    url="https://github.com/bo-dun-1/feathery-python-server-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)