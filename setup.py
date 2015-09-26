import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    name="django-podcasting",
    version=__import__("podcasting").__version__,
    url="http://django-podcasting.readthedocs.org/",
    license="BSD",
    description="Audio podcasting functionality for django sites.",
    long_description=read("README.rst"),
    author="Thomas Schreiber",
    author_email="tom@nillab.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django-model-utils>=2.3.1",
        "django-appconf>=1.0.1",
        "django-autoslug>=1.8.0",
    ],
    tests_require=[
        "Django>=1.6",
        "django-autoslug>=1.8.0",
        "Pillow>=2.9.0",
        "factory_boy>=2.5.2",
    ],
    test_suite="runtests.runtests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False,
)
