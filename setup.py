from setuptools import setup, find_packages

requirements = ["pandas", "numpy"]

setup(
    name="origin",
    version="0.0.1",
    install_requires=requirements,
    packages=find_packages(),
)