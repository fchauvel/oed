#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from oed.library import Packages
from oed.laboratory import Experiment, Laboratory



class TestingSession:

    def __init__(self, oed):
        self._oed = oed
        self._target_requirements = []

    def add(self, requirements):
        for any_requirement in requirements:
            self._target_requirements.append(any_requirement)

    def start(self):
        for each_requirement in self._target_requirements:
            for each_candidate_release in  each_requirement.candidate_releases:
                self._oed.start_experiment("sphinx", # Fake
                                           "1.0", # Fake
                                           each_requirement, 
                                           each_candidate_release)



class OeD:

    def __init__(self, packages=None, laboratory=None):
        self._packages = packages or Packages()
        self._laboratory = laboratory or Laboratory()

    def select(self, source_name, source_version, target_name):
        target = self._packages.find_package(target_name)
        release = self._packages.find_release(source_name, source_version)
        return release.find_requirements_for(target)

    def new_testing_session(self):
        return TestingSession(self)

    @property
    def experiments(self):
        return self._laboratory.experiments

    def start_experiment(self, source_package, source_release, requirement, selected_release):
        experiment = self._laboratory.new_experiment(
            source_package,
            source_release,
            requirement.required_package.name,
            selected_release.name
        )
        experiment.start()