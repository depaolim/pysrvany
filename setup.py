from setuptools import setup


setup(
    name='pysrvany',
    version='0.0.1',
    description='Run Windows Executables as Services',
    license="MIT",
    author='Marco De Paoli',
    author_email='depaolim@gmail.com',
    url="https://github.com/depaolim/pysrvany",
    packages=['pysrvany'],
    install_requires=[],  # external packages as dependencies
    scripts=['pysrvany_cli.py']
)
