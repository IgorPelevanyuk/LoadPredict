from setuptools import setup, find_packages

setup(
    name='LoadPredict',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    extras_require={"tests": "pytest"},
    url='',
    license='',
    author='ipelevan',
    author_email='gavelock@gmail.com',
    description='LoadPrediction on distributed computing infrastructure'
)
