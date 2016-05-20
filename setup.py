import setuptools

with open("requirements.txt") as reqs:
    install_requires = reqs.readlines()

setuptools.setup(
    name="correios",
    version="0.2.0",
    url="https://github.com/osantana/correios",

    author="Osvaldo Santana Neto",
    author_email="correiospy@osantana.me",

    description="A client library for Brazilian Correios APIs and services",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=install_requires,

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
