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
from oed.engines.vcs import RepositoryFactory

from os import chdir, getcwd
from os.path import abspath, exists, join

from re import search, findall

from urllib.request import build_opener



class OSPlatform(Platform):


    def __init__(self, workspace=None, repositories=None):
        super().__init__()
        self._workspace = workspace or "tmp-test"
        self._repositories = repositories or RepositoryFactory()

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
        repository = self._check_vcs_url(experiment)
        with open(self._path_to_script, "w+") as script:
            script.write("git clone {vcs_url} sources\n".format(vcs_url=repository.clone_URL))
            script.write("cd sources\n")
            
            script.write("git fetch tags/{tag} -b sut\n"\
                         .format(tag=repository.find_tag_for("2.4.4")))
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


    def _check_vcs_url(self, experiment):
        url = experiment._vcs_url
        repository = self._repositories.from_URL(url)
        if repository:
            return repository
        else:
            content = self._fetch_content(url)
            for any_url in self._extract_all_urls(content):
                repository = self._repositories.from_URL(any_url)
                if repository:
                    return repository
            else:
                raise RuntimeError("Could not find a VCS URL!")
        

    def _fetch_content(self, url):
        print("URL: ", url)
        opener = build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        data = opener.open(url).read().decode("ISO-8859-1", errors="ignore")
        return data

    
    def _extract_all_urls(self, content):
        matches = findall(self.URL_PATTERN, content)
        return ["".join(m) for m in matches]

    URL_PATTERN = r'(http|ftp|https)(://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'


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


    
class OutputReader:

    def __init__(self):
        self._extractors = []

    def _create(self, pattern):
        extractor = Extractor(pattern)
        self._extractors.append(extractor)
        return extractor

    def extract_results(self, output, results):
        for each_line in output:
            for each_extractor in self._extractors:
                each_extractor.scrutinize(each_line)
        self._fill_in(results)

    def _fill_in(self, results):
        pass



class  PyTestReader(OutputReader):

    def __init__(self):
        super().__init__()
        self._passed = self._create("(\\d+) passed")
        self._xpassed = self._create("(\\d+) xpassed")
        self._failed = self._create("(\\d+) failed")
        self._xfailed = self._create("(\\d+) xfailed")
        self._skipped = self._create("(\\d+) skipped")
        self._error = self._create("(\\d+) errors?")

    def _fill_in(self, results):
        results.set_passed_tests_count(self._passed.value \
                                       + self._xfailed.value)
        results.set_skipped_tests_count(self._skipped.value)
        results.set_failed_tests_count(self._failed.value \
                                       + self._xpassed.value)
        results.set_error_tests_count(self._error.value)



class CoverageReader(OutputReader):

    def __init__(self):
        super().__init__()
        self._coverage = \
            self._create("TOTAL\\s+\\d+\\s+\\d+\\s+\\d+\\s+\\d+\\s+(\\d+)%")
    def _fill_in(self, results):
        results.set_test_coverage(self._coverage.value)


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
