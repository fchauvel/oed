#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from setuptools import setup, find_packages


test_dependencies = [
    "green==2.15.0",
    "mock==2.0.0",
    "coverage==4.5.3"
]

setup(name="oed",
      version="0.0.1",
      description="Analyser of open-ended dependencies",
      author="Franck Chauvel",
      author_email="franck.chauvel@sintef.no",
      url="https://github.com/STAMP-project/camp",
      packages=find_packages(exclude=["tests*", "tests.*"]),
      license="MIT",
      test_suite="tests",
      entry_points = {
          'console_scripts': [
              'oed = oed.run:main'
          ]
      },
      install_requires = [
          "argparse == 1.2.1",
      ],
      tests_require = test_dependencies,
      extras_require = {
          "test": test_dependencies
      },
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Testing"
      ],
)
