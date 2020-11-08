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
                experiment = Experiment("sphinx", "1.0", each_requirement, each_candidate_release)
                self._oed.start_experiment(experiment)


class Experiment:

    def __init__(self, source, release, requirement, selected_candidate):
        pass


class OeD:

    def __init__(self, packages):
        self._packages = packages
        self._experiments = [] #Fake

    def select(self, source_name, source_version, target_name):
        target = self._packages.find_package(target_name)
        release = self._packages.find_release(source_name, source_version)
        return release.find_requirements_for(target)

    def new_testing_session(self):
        return TestingSession(self)

    def experiments(self):
        return []

    def start_experiment(self, experiment):
        self._experiments.append(experiment) # Fake