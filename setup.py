from setuptools import setup, find_packages
from disappeer import metainfo


setup(
    name='disappeer',
    version=metainfo.version,
    description='A pure Python GUI app that provides access to gnupg, and P2P GPG-encrypted messaging over Tor',
    author='Disappeer Labs',
    author_email=metainfo.email,
    license='GPLv3',
    packages=find_packages(exclude=('tests',)),
    entry_points={
        'console_scripts': [
            'disappeer = disappeer.__main__:main'
        ]
    }
)
