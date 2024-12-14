from setuptools import setup, find_packages

setup(
    name="groheblue",
    version="0.3.2",
    description="A python package for interacting with the Grohe Blue API.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Konstantin Weber",
    license="MIT",
    url="https://github.com/koproductions-code/groheblue",
    project_urls={
        "GitHub": "https://github.com/koproductions-code/groheblue",
    },
    packages=find_packages(),
    install_requires=[
        "bs4==0.0.2",
        "httpx>=0.27.0",
    ],
    python_requires=">=3.6",
)
