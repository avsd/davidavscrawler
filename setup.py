#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Scrapy==1.0.1',
]

test_requirements = [
    'mock==1.3.0',
]

setup(
    name='davidavscrawler',
    version='0.1.0',
    description="Simple crawler generating a sitemap.",
    long_description=readme,
    author="David Avs",
    author_email='david@davidavs.com',
    url='https://github.com/avsd/davidavscrawler',
    packages=[
        'davidavscrawler',
    ],
    package_dir={'davidavscrawler':
                 'davidavscrawler'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='davidavscrawler',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': ['crawl=davidavscrawler.crawler:main'],
    },
)
