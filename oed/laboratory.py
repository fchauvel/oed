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


class Results:

    def __init__(self, passed_count, skipped_count=0, failed_count=0, error_count=0):
        self._passed_count = passed_count
        self._skipped_count = skipped_count
        self._failed_count = failed_count
        self._error_count = error_count

    @property
    def test_count(self):
        return self._passed_count + self._skipped_count \
                + self._failed_count + self._error_count


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