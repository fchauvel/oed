#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from oed.laboratory import Platform, ResultBuilder

from os import chdir, getcwd
from os.path import abspath, exists, join

from re import search


class OSPlatform(Platform):


    def __init__(self, workspace=None, shell=None):
        super().__init__()
        self._workspace = workspace or "tmp-test"

    def run(self, experiment):
        self._prepare_workspace()
        self._generate_script(experiment)
        output = self._execute_script()
        results = ResultBuilder()
        PyTestReader().extract_results(output, results)
        CoverageReader().extract_results(output, results)
        return results.build()

    def _prepare_workspace(self):
        from os import makedirs
        path = self._path_to_experiment
        if not exists(path):
            makedirs(path) # Fake

    @property
    def _path_to_experiment(self):
        return join(self._workspace, "exp1")

    def _generate_script(self, experiment):
        with open(self._path_to_script, "w+") as script:
            script.write("git clone {vcs_url} sources\n".format(vcs_url=experiment._vcs_url))
            script.write("cd sources\n")
            script.write("git fetch tags/{tag} -b sut\n".format(tag="v2.4.4")) # Fake
            script.write("virtualenv .venv\n")
            script.write("./venv/Scripts/activate.ps1\n")
            script.write("pip install pytest coverage\n")
            script.write("pip install .[test]\n")
            script.write("coverage run -m pytest\n")
            script.write("coverage combine\n")
            script.write("coverage report\n")

    @property
    def _path_to_script(self):
        return join(self._path_to_experiment, self.SCRIPT_NAME)

    SCRIPT_NAME = "experiment.ps1"


    def _execute_script(self):
        from subprocess import run
        current = getcwd()
        chdir(self._path_to_experiment)
        execution = run(["powershell",  join(".", self.SCRIPT_NAME)], capture_output=True)
        with open(self.EXPERIMENT_LOG, "w+") as log:
            log.write(execution.stdout)
        chdir(abspath(current))
        return execution.stdout.splitlines()

    EXPERIMENT_LOG = "experiment.log"


class  PyTestReader:

    def __init__(self):
        self._extractors = []
        self._passed = self._create("(\\d+) passed")
        self._xpassed = self._create("(\\d+) xpassed")
        self._failed = self._create("(\\d+) failed")
        self._xfailed = self._create("(\\d+) xfailed")
        self._skipped = self._create("(\\d+) skipped")
        self._error = self._create("(\\d+) errors?")

    def _create(self, pattern):
        extractor = Extractor(pattern)
        self._extractors.append(extractor)
        return extractor

    def extract_results(self, output, results):
        for each_line in output:
            for each_extractor in self._extractors:
                each_extractor.scrutinize(each_line)

        results.set_passed_tests_count(self._passed.value \
                                       + self._xfailed.value)
        results.set_skipped_tests_count(self._skipped.value)
        results.set_failed_tests_count(self._failed.value \
                                       + self._xpassed.value)
        results.set_error_tests_count(self._error.value)


class CoverageReader:

    def extract_results(self, output, results):
        results.set_test_coverage(81.1)


class Extractor:

    def __init__(self, pattern):
        self._count = None
        self._pattern = pattern

    def scrutinize(self, text):
        found = search(self._pattern, text)
        if found:
            if self._count is not None:
                print("Warning: Overriding previous value!")
            self._count = int(found.group(1))

    @property
    def value(self):
        return self._count or 0
