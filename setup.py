from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="customer-metrics-for-postpay",
    version="1.0.0",
    author="Anjala Abdul Rehman",
    author_email="anjala.lahan@gmail.com",
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
)