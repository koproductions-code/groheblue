from setuptools import setup, find_packages

setup(
    name="groheblue",
    version="0.1.0",
    description="A python package for interacting with the Grohe Blue API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Konstantin Weber",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "aiohttp==3.10.10",
        "bs4==0.0.2",
        "httpx==0.27.2",
    ],
    python_requires=">=3.6",
)
