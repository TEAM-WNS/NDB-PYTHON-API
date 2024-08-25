from setuptools import setup, find_packages

setup(
    name='ndb_python_api',
    version='{{VERSION_PLACEHOLDER}}',
    author= 'fireing123',
    author_email= 'gimd82368@gmail.com',
    url= 'https://github.com/TEAM-WNS/NDB-PYTHON-API',
    packages=find_packages(),
    long_description=open('README.md', 'r', encoding="UTF8").read(),
    long_description_content_type='text/markdown',
)
