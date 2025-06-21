#! -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

def get_requires() -> list[str]:
    with open("requirements.txt", encoding="utf-8") as f:
        file_content = f.read()
        lines = [line.strip() for line in file_content.strip().split("\n") if not line.startswith("#")]
        return lines

extra_require = {
    "seaborn": ["seaborn"],
    "matplotlib": ["matplotlib"],
    "sklearn": ["sklearn"],
    "xgboost": ["xgboost"],
    "sklearn": ["sklearn"]
}


setup(
    name='pd4anal',
    version='v0.0.1',
    description='an elegant pd4anal',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT Licence',
    url='https://github.com/Tongjilibo/pd4anal',
    author='Tongjilibo',
    install_requires=get_requires(),
    extras_require=extra_require,
    packages=find_packages()
)