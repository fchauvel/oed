#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from oed.os import Shell

from traceback  import print_exc



class Experiment:

    def __init__(self, platform, source_package_name, source_release_name, required_package_name, target_release_name):
        self._platform = platform
        self._source_package_name = source_package_name
        self._source_release_name = source_release_name
        self._required_package_name  = required_package_name
        self._target_release_name = target_release_name
        self._vcs_url = "https://github.com/sphinx-doc/sphinx.git"
        self._subject = "{}=={}".format(source_package_name, source_release_name)
        self._object = "{}=={}".format(required_package_name, target_release_name)
        self._test_results = None


    def start(self):
        self._test_results = self._platform.run(self)

    @property
    def subject(self):
        return self._subject

    @property
    def object(self):
        return self._object

    @property
    def is_complete(self):
        return self._test_results is not None

    @property
    def results(self):
        return self._test_results



class ResultBuilder:

    def __init__(self):
        self._passed_tests_count = None
        self._failed_tests_count = None
        self._skipped_tests_count = None
        self._error_tests_count = None
        self._coverage = None

    def set_passed_tests_count(self, count):
        self._passed_tests_count = count

    def set_failed_tests_count(self, count):
        self._failed_tests_count = count

    def set_skipped_tests_count(self, count):
        self._skipped_tests_count = count

    def set_error_tests_count(self, count):
        self._error_tests_count = count

    def set_test_coverage(self, coverage_percent):
        self._coverage = coverage_percent

    def build(self):
        return Results(TestResults(self._passed_tests_count,
                                   self._skipped_tests_count,
                                   self._failed_tests_count,
                                   self._error_tests_count,
                                   self._coverage))

class Results:


    def __init__(self, test_results):
        self._test_results = test_results

    @property
    def tests(self):
        return self._test_results



class TestResults:

    def __init__(self, passed_count,
                 skipped_count=0,
                 failed_count=0,
                 error_count=0,
                 coverage=None):
        self._passed_count = passed_count
        self._skipped_count = skipped_count
        self._failed_count = failed_count
        self._error_count = error_count
        self._coverage = coverage

    @property
    def count(self):
        return self._passed_count + self._skipped_count \
                + self._failed_count + self._error_count

    @property
    def coverage(self):
        return self._coverage


    
class Platform:
    """Hides the way the experiment is run (e.g., locally, remotely, using Docker, using virtualenv)"""

    def run(self, experiment):
        pass



class Experiments:

    def __init__(self, experiments=None):
        self._experiments = experiments or []

    def select(self, predicate):
        selection = []
        for any_experiment in self._experiments:
            if predicate(any_experiment):
                selection.append(any_experiment)
        return selection

    def store(self, experiment):
        self._experiments.append(experiment)



class Laboratory:

    def __init__(self, experiments=None, platform=None):
        self._experiments = experiments or Experiments()
        self._platform = platform

    def new_experiment(self, source_package_name, source_release_name, required_package_name, required_release_name):
        experiment = Experiment(self._platform,
                                source_package_name,
                                source_release_name,
                                required_package_name,
                                required_release_name)
        self._experiments.store(experiment)
        return experiment

    @property
    def experiments(self):
        return self._experiments
