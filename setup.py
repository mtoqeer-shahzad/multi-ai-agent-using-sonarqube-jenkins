from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Multi-Agent-AI-System',
    version='0.1',
    author='toqeer',
    packages=find_packages(),       # ✅ added ()
    install_requires=requirements   # ✅ changed requires → install_requires
)