# Copyright 2016 Osvaldo Santana Neto
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from setuptools import find_packages, setup


def load_requirements(filename):
    install_requires = {}
    section = "install_requires"

    reqs = open(filename)
    for raw_line in reqs:
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("#"):
            section = line.replace("#", "").strip()
            continue

        install_requires.setdefault(section, []).append(line)

    return install_requires


requirements = load_requirements("requirements.txt")

setup(
    name="correios",
    version="6.1.19",
    url="https://github.com/osantana/correios",
    author="Osvaldo Santana Neto",
    author_email="correiospy@osantana.me",
    description="A client library for Brazilian Correios APIs and services",
    long_description=open("README.rst").read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements.pop("install_requires"),
    extras_require=requirements,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    entry_points={"console_scripts": ["update-correios-wsdl=correios.update_wsdl:cli"]},
)
