#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



class Experiment:

    def __init__(self, laboratory, source_package_name, source_release_name, requirement, target_package):
        self._laboratory = laboratory

    def start(self):
        return self._laboratory.start(self)


class Laboratory:

    def __init__(self, experiments=None):
        self._experiments = experiments or []

    def  new_experiment(self, source_package_name, source_release_name, requirement, target_package):
        return Experiment(self, source_package_name, source_release_name, requirement, target_package)

    @property
    def experiments(self):
        return self._experiments

    def start(self, experiment):
        self._experiments.append(experiment)